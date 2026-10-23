"""OAuth for an app installed on Talki accounts: the consent URL, the code
exchange, refresh, revocation, and an access token that renews itself.

    from talki import Talki
    from talki.oauth import OAuthApp, Pkce, authorization_url, read_callback

    app = OAuthApp(client_id, client_secret)
    pkce, state = Pkce.new(), secrets.token_urlsafe(16)
    url = authorization_url(client_id, redirect_uri, ["calls:read"], state=state, pkce=pkce)
    # … send the browser to url; on the callback:
    code = read_callback(callback_url, state=state)
    tokens = app.exchange_code(code, redirect_uri=redirect_uri, code_verifier=pkce.verifier)
    save(tokens)

    talki = Talki(tokens=tokens, oauth_app=app, on_token_refresh=save)

`/oauth/token` and `/oauth/revoke` answer in RFC 6749's shape
(`{"error", "error_description"}`), raised here as `OAuthError`.

**A refresh token rotates on every use.** Store the new pair before the new
access token is used: `on_token_refresh` is called with it, and the request
waits for it. Presenting a rotated refresh token again revokes the whole
installation, so refreshes made through one `Talki` are serialised; never
refresh one pair from two processes.

The server takes a rotated refresh token once more within `REFRESH_GRACE`
seconds of its rotation, as the retry of a refresh whose answer was lost. So a
refresh whose outcome is unknown is presented again within the same request,
once the first has had `REFRESH_SETTLE` seconds to finish. When that would
fall outside the grace (a timeout above 45 seconds), the request raises; the
next one presents the token again, which works only if the first never reached
the server. Otherwise the customer has to reconnect.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import logging
import secrets
import threading
import time
from collections.abc import AsyncGenerator, Awaitable, Callable, Generator
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import parse_qs, quote_plus, urlencode, urlsplit

import anyio
import httpx

from ._transport import GATEWAY_STATUSES, NOT_SENT, UNSENT_ONLY
from ._version import USER_AGENT
from .exceptions import REQUEST_ID_HEADER, TalkiError

# Under the `talki` logger: renewals and their failures, never a token.
logger = logging.getLogger(__name__)

__all__ = [
    "DEFAULT_AUTHORIZE_URL",
    "DEFAULT_ISSUER",
    "OAuthApp",
    "OAuthError",
    "Pkce",
    "TokenRefresh",
    "TokenSet",
    "authorization_url",
    "read_callback",
]

DEFAULT_AUTHORIZE_URL = "https://app.talki.it/autorizza"
DEFAULT_ISSUER = "https://api.talki.it"
# Renew an access token this many seconds before it expires.
REFRESH_LEEWAY = 60.0
# How long after a refresh token's first rotation the server takes it once
# more, as the retry of a refresh whose answer was lost. Later, presenting it
# revokes the installation.
REFRESH_GRACE = 60.0
# After a refresh whose outcome is unknown (sent, then its answer lost, timed
# out, or a gateway's 5xx), wait this long before presenting the same refresh
# token again: long enough for the first to finish on the server, so the second
# is not an overlap (which revokes the pair), and well inside REFRESH_GRACE.
REFRESH_SETTLE = 10.0
# A refresh is presented again within the same request only if it goes out
# this long before the grace ends, counted from the first send: room for it to
# reach the server.
GRACE_MARGIN = 5.0
# Under an event loop other than asyncio, an async renewal waiting for another
# polls the lock: first after this long, then twice as long each time.
LOCK_POLL = 0.01
LOCK_POLL_MAX = 0.5


class OAuthError(TalkiError):
    """An RFC 6749 error, from the token endpoints or on the callback."""

    def __init__(
        self, error: str, description: str = "", *, status: int | None = None, request_id: str | None = None
    ) -> None:
        self.error = error
        self.description = description
        self.status = status
        self.request_id = request_id
        super().__init__(f"{error}: {description}" if description else error)

    def __reduce__(self) -> tuple[Any, ...]:
        return (_restore_oauth_error, (self.error, self.description, self.status, self.request_id))


def _restore_oauth_error(error: str, description: str, status: int | None, request_id: str | None) -> OAuthError:
    return OAuthError(error, description, status=status, request_id=request_id)


@dataclass(frozen=True)
class Pkce:
    """A PKCE pair: send `challenge` in the consent URL, `verifier` with the code."""

    verifier: str = field(repr=False)
    challenge: str

    @classmethod
    def new(cls) -> Pkce:
        verifier = secrets.token_urlsafe(48)  # 64 characters: inside RFC 7636's 43–128
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        return cls(verifier=verifier, challenge=base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii"))


@dataclass(frozen=True)
class TokenSet:
    """One installation's token pair, as `/oauth/token` answers it."""

    access_token: str = field(repr=False)
    refresh_token: str = field(repr=False)
    expires_at: float | None = None
    scopes: tuple[str, ...] = ()
    account_id: str = ""
    installation_id: str = ""
    livemode: bool = True

    @classmethod
    def from_body(cls, body: dict[str, Any], *, now: float | None = None) -> TokenSet:
        expires_in = body.get("expires_in")
        issued = time.time() if now is None else now
        return cls(
            access_token=str(body["access_token"]),
            refresh_token=str(body["refresh_token"]),
            expires_at=issued + float(expires_in) if isinstance(expires_in, (int, float)) else None,
            # Space-delimited, per RFC 6749 §5.1.
            scopes=tuple(str(body.get("scope") or "").split()),
            account_id=str(body.get("account_id") or ""),
            installation_id=str(body.get("installation_id") or ""),
            livemode=bool(body.get("livemode", True)),
        )


def authorization_url(
    client_id: str,
    redirect_uri: str,
    scopes: list[str],
    *,
    state: str,
    pkce: Pkce,
    prompt: str | None = None,
    enrollment: str | None = None,
    authorize_url: str = DEFAULT_AUTHORIZE_URL,
) -> str:
    """The consent page to send the customer's browser to. ``prompt="consent"``
    replaces the grant with exactly ``scopes``; ``enrollment`` carries a billing
    partner's activation."""
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "state": state,
        "code_challenge": pkce.challenge,
        "code_challenge_method": "S256",
    }
    if prompt:
        params["prompt"] = prompt
    if enrollment:
        params["enrollment"] = enrollment
    return f"{authorize_url}?{urlencode(params)}"


def read_callback(url: str, *, state: str, issuer: str = DEFAULT_ISSUER) -> str:
    """The code on the callback URL (or its query string). Raises `OAuthError`
    for a `state` that is not yours, an `iss` that is not Talki's, or a
    refusal (`access_denied` when the customer declines)."""
    if not state:
        raise ValueError("Pass the state sent in the consent URL.")
    query = {key: values[0] for key, values in parse_qs(urlsplit(url).query or url.lstrip("?")).items()}
    if not secrets.compare_digest(query.get("state", "").encode(), state.encode()):
        raise OAuthError("state_mismatch", "The callback's state is not the one sent.")
    if query.get("iss", "").rstrip("/") != issuer.rstrip("/"):
        raise OAuthError("issuer_mismatch", "The callback's iss is not Talki's.")
    if "error" in query:
        raise OAuthError(query["error"], query.get("error_description", ""))
    if "code" not in query:
        raise OAuthError("missing_code", "The callback carries neither a code nor an error.")
    return query["code"]


def _failure(response: httpx.Response) -> OAuthError:
    try:
        body = response.json()
    except ValueError:
        body = None
    request_id = response.headers.get(REQUEST_ID_HEADER)
    if isinstance(body, dict) and isinstance(body.get("error"), str):
        return OAuthError(
            body["error"], str(body.get("error_description") or ""), status=response.status_code, request_id=request_id
        )
    return OAuthError("unexpected_response", response.text[:300], status=response.status_code, request_id=request_id)


def _tokens(response: httpx.Response, *, now: float | None = None) -> TokenSet:
    if not response.is_success:
        raise _failure(response)
    return TokenSet.from_body(response.json(), now=now)


class OAuthApp:
    """An app's credentials, for the token endpoints. Client authentication is
    HTTP Basic."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        base_url: str = DEFAULT_ISSUER,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.client_id = client_id
        self._client_secret = client_secret
        self.base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._transport = transport

    def __repr__(self) -> str:
        return f"OAuthApp(client_id={self.client_id!r})"

    @property
    def token_url(self) -> str:
        return f"{self.base_url}/oauth/token"

    def _basic(self) -> str:
        # Each half form-encoded first, as RFC 6749 §2.3.1 asks.
        pair = f"{quote_plus(self.client_id)}:{quote_plus(self._client_secret)}".encode()
        return "Basic " + base64.b64encode(pair).decode("ascii")

    def token_request(self, form: dict[str, str], path: str = "/oauth/token") -> httpx.Request:
        return httpx.Request(
            "POST",
            f"{self.base_url}{path}",
            data=form,
            headers={"Authorization": self._basic(), "Accept": "application/json", "User-Agent": USER_AGENT},
        )

    def _send(self, request: httpx.Request) -> httpx.Response:
        with httpx.Client(timeout=self._timeout, transport=self._transport) as client:
            return client.send(request)

    def exchange_code(self, code: str, *, redirect_uri: str, code_verifier: str) -> TokenSet:
        """The pair for a callback's code. A code works once: presenting it again
        revokes the installation, so never retry this with the same code."""
        form = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
        }
        return _tokens(self._send(self.token_request(form)))

    def refresh(self, refresh_token: str, *, scopes: list[str] | None = None) -> TokenSet:
        """A new pair. The old refresh token stops working: store the new one first."""
        form = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        if scopes:
            form["scope"] = " ".join(scopes)
        return _tokens(self._send(self.token_request(form)))

    def revoke(self, token: str) -> None:
        """Disconnect the installation (RFC 7009): either half of a pair revokes both."""
        response = self._send(self.token_request({"token": token}, "/oauth/revoke"))
        if not response.is_success:
            raise _failure(response)


class TokenRefresh(httpx.Auth):
    """httpx authentication that sends the current access token, and renews the
    pair shortly before it expires, or when the API answers that it has.

    `Talki(tokens=…, oauth_app=…)` builds one; `tokens` is always the latest pair.

    One lock serialises every renewal through this object, from threads, event
    loops and sync and async calls alike: presenting a rotated refresh token
    again revokes the installation. Async callers wait for it without blocking
    their loop.

    A refresh whose outcome is unknown (its answer lost, timed out, or a
    gateway's 502, 503 or 504) may have rotated the pair on the server. The
    same refresh token is presented again `REFRESH_SETTLE` seconds later, so
    as not to overlap the first, within the same request as long as that is
    inside the server's `REFRESH_GRACE`; otherwise on the next request, which
    takes it only if nothing reached the server the first time. That needs
    ``transport``, the one the client sends on (`Talki` passes its own):
    refreshes then go out on it directly, and a failure is seen for what it
    is. Without it they go through the client, which closes this flow on a
    failure without saying which: the next request presents again.
    """

    def __init__(
        self,
        tokens: TokenSet,
        app: OAuthApp,
        *,
        on_refresh: Callable[[TokenSet], None] | None = None,
        leeway: float = REFRESH_LEEWAY,
        clock: Callable[[], float] = time.time,
        transport: httpx.BaseTransport | httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.tokens = tokens
        self._app = app
        self._on_refresh = on_refresh
        self._leeway = leeway
        self._clock = clock
        self._transport = transport
        self._lock = threading.Lock()
        # The thread holding the lock, and whether synchronously, to refuse
        # re-entry rather than deadlock.
        self._owner: int | None = None
        self._owner_sync = False
        # Async waiters for the lock, each woken from whichever thread
        # releases it.
        self._wakers: set[Callable[[], None]] = set()
        self._wakers_lock = threading.Lock()
        # On a clock that never steps back: when the last refresh was sent;
        # when a refresh's outcome last became unknown; and when the first
        # refresh still of unknown outcome was sent, which is before the server
        # could have rotated the pair and started its grace.
        self._monotonic: Callable[[], float] = time.monotonic
        self._sent_at = 0.0
        self._in_doubt_since: float | None = None
        self._doubt_sent: float | None = None
        self._sleep: Callable[[float], None] = time.sleep
        self._async_sleep: Callable[[float], Awaitable[None]] = anyio.sleep
        # A pair the API issued that could not be stored yet: the only live one.
        self._pending: TokenSet | None = None
        # Set once the API refused the refresh token or the app's credentials:
        # every request fails fast, without spending the token endpoint's limits.
        self._dead: OAuthError | None = None

    # Decisions, under the lock.

    def _due(self) -> bool:
        expires_at = self.tokens.expires_at
        return self._pending is not None or (expires_at is not None and self._clock() >= expires_at - self._leeway)

    def _wanted(self, retry: bool, sent: str | None) -> bool:
        """Under the lock: store a pair still pending, and say whether to
        refresh: when the pair is due, or, for a request the API answered
        that its token expired, when no one renewed it meanwhile."""
        self._check()
        if self._pending is not None:
            self._store(self._pending)
            return False
        return self.tokens.access_token == sent if retry else self._due()

    @staticmethod
    def _rejected(response: httpx.Response) -> bool:
        return response.status_code == 401 and 'error="invalid_token"' in response.headers.get("WWW-Authenticate", "")

    def _presentation(self, request: httpx.Request) -> httpx.Request:
        """The refresh to send now, with the caller's timeout (none would wait
        forever, holding the lock) and nothing else of its extensions."""
        refresh = self._app.token_request({"grant_type": "refresh_token", "refresh_token": self.tokens.refresh_token})
        refresh.extensions = {UNSENT_ONLY: True}
        if "timeout" in request.extensions:
            refresh.extensions["timeout"] = request.extensions["timeout"]
        self._sent_at = self._monotonic()
        return refresh

    def _settle_delay(self) -> float:
        """How long to wait before presenting a refresh token whose last
        presentation has an unknown outcome: timed from when the outcome was
        lost, since a timeout comes long after the send."""
        if self._in_doubt_since is None:
            return 0.0
        return max(0.0, REFRESH_SETTLE - (self._monotonic() - self._in_doubt_since))

    def _lost(self, error: BaseException | None) -> bool:
        """Record a refresh that ended in ``error``, or (None) in a gateway's
        5xx, and say whether to present it again in this flow, after
        `_settle_delay`."""
        if isinstance(error, NOT_SENT):
            # Nothing reached the server: as much in doubt as before.
            return False
        now = self._monotonic()
        self._in_doubt_since = now
        if self._doubt_sent is None:
            self._doubt_sent = self._sent_at
        cause = "a gateway error" if error is None else type(error).__name__
        if error is not None and not isinstance(error, httpx.TransportError):
            # Abandoned (cancelled, interrupted, closed by httpx), or a failure
            # that is not the network's: not one to repeat here.
            logger.warning(
                "A token renewal ended in %s, its outcome unknown; the next request presents it again.", cause
            )
            return False
        again = now + REFRESH_SETTLE <= self._doubt_sent + REFRESH_GRACE - GRACE_MARGIN
        logger.warning(
            "A token renewal ended in %s, its outcome unknown; %s.",
            cause,
            f"presenting it again in {REFRESH_SETTLE:.0f} s" if again else "the next request presents it again",
        )
        return again

    def _answered(self, response: httpx.Response) -> bool:
        """Apply a refresh's answer, or say (False) to present it again. A
        gateway's 502, 503 or 504 does not say whether the refresh ran: the
        app may have rotated the pair and then died."""
        if response.status_code in GATEWAY_STATUSES:
            if self._lost(None):
                return False
            raise _failure(response)
        self._in_doubt_since = self._doubt_sent = None
        self._apply(response)
        return True

    def _store(self, renewed: TokenSet) -> None:
        """Hand the pair to `on_refresh`, then use it. If storing fails it stays
        pending: the next request stores it first, never refreshing again with
        the refresh token it replaced."""
        self._pending = renewed
        if self._on_refresh is not None:
            self._on_refresh(renewed)
        self.tokens, self._pending = renewed, None
        logger.info("Renewed the access token of installation %s.", renewed.installation_id or "(unnamed)")

    def _apply(self, response: httpx.Response) -> None:
        try:
            renewed = _tokens(response, now=self._clock())
        except OAuthError as error:
            if error.error in ("invalid_grant", "invalid_client"):
                logger.error(
                    "The API refused the token renewal (%s): %s",
                    error.error,
                    "the customer has to reconnect the app"
                    if error.error == "invalid_grant"
                    else "check the app's client ID and secret",
                )
                self._dead = error
            raise
        self._store(renewed)

    def _check(self) -> None:
        dead = self._dead
        if dead is not None:
            # A new instance each time: re-raising one would grow its traceback.
            raise OAuthError(dead.error, dead.description, status=dead.status, request_id=dead.request_id)

    def _authorize(self, request: httpx.Request) -> str:
        token = self.tokens.access_token
        request.headers["Authorization"] = f"Bearer {token}"
        return token

    # The lock, refusing re-entry from the thread that holds it: from
    # `on_refresh`, or a sync call made on the loop thread of an async renewal.

    _REENTRY = (
        "This Talki is renewing its token on this thread: do not call it from on_token_refresh, "
        "or synchronously from async code using it."
    )

    def _enter(self) -> None:
        if self._owner == threading.get_ident():
            raise RuntimeError(self._REENTRY)
        self._lock.acquire()
        self._owner, self._owner_sync = threading.get_ident(), True

    def _leave(self) -> None:
        self._owner, self._owner_sync = None, False
        self._lock.release()
        with self._wakers_lock:
            wakers = list(self._wakers)
        for wake in wakers:
            wake()

    # Sync.

    def _send(self, refresh: httpx.Request) -> httpx.Response | None:
        """Send a refresh on the transport: its answer, read, or None to
        present it again."""
        transport = self._transport
        if not isinstance(transport, httpx.BaseTransport):
            raise TypeError("The transport given is async only; this client was used synchronously.")
        try:
            response = transport.handle_request(refresh)
            try:
                response.read()
            finally:
                response.close()
        except BaseException as error:
            if self._lost(error):
                return None
            raise
        return response

    def _sync_refresh(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Under the lock: present the refresh token until an answer settles it."""
        while True:
            delay = self._settle_delay()
            if delay:
                self._sleep(delay)
            refresh = self._presentation(request)
            if self._transport is not None:
                response = self._send(refresh)
            else:
                try:
                    response = yield refresh
                    response.read()
                except BaseException as error:
                    # httpx closes this flow when the send fails, without
                    # saying how: GeneratorExit, taken as maybe sent.
                    self._lost(error)
                    raise
            if response is not None and self._answered(response):
                return

    def sync_auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        # Kept in memory: a request answered 401 is sent again.
        request.read()
        self._check()
        sent: str | None = None
        for retry in (False, True):
            if retry or self._due():
                self._enter()
                try:
                    if self._wanted(retry, sent):
                        yield from self._sync_refresh(request)
                finally:
                    self._leave()
            sent = self._authorize(request)
            response = yield request
            if retry or not self._rejected(response):
                return
            # Read before waiting, so this connection goes back to the pool.
            response.read()

    # Async: the same lock, waited for without blocking the loop.

    def _on_release(self) -> tuple[asyncio.Future[None], Callable[[], None]] | None:
        """Under asyncio, a future resolved the next time the lock is released,
        by whichever thread. None under another event loop, which polls."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return None
        released: asyncio.Future[None] = loop.create_future()

        def resolve() -> None:
            if not released.done():
                released.set_result(None)

        def wake() -> None:
            try:
                loop.call_soon_threadsafe(resolve)
            except RuntimeError:
                pass  # That loop has closed: no one is waiting there.

        with self._wakers_lock:
            self._wakers.add(wake)
        return released, wake

    async def _aenter(self) -> None:
        poll = LOCK_POLL
        while True:
            # Listening before trying, so a release in between is not missed.
            waiter = self._on_release()
            try:
                if self._lock.acquire(blocking=False):
                    break
                if self._owner == threading.get_ident() and self._owner_sync:
                    # A synchronous renewal below us on this thread: it cannot
                    # finish while we wait.
                    raise RuntimeError(self._REENTRY)
                if waiter is not None:
                    await waiter[0]
                else:
                    await self._async_sleep(poll)
                    poll = min(poll * 2, LOCK_POLL_MAX)
            finally:
                if waiter is not None:
                    with self._wakers_lock:
                        self._wakers.discard(waiter[1])
        self._owner, self._owner_sync = threading.get_ident(), False

    async def _asend(self, refresh: httpx.Request) -> httpx.Response | None:
        """`_send`, async."""
        transport = self._transport
        if not isinstance(transport, httpx.AsyncBaseTransport):
            raise TypeError("The transport given is sync only; this client was used asynchronously.")
        try:
            response = await transport.handle_async_request(refresh)
            try:
                await response.aread()
            finally:
                await response.aclose()
        except BaseException as error:
            if self._lost(error):
                return None
            raise
        return response

    async def async_auth_flow(self, request: httpx.Request) -> AsyncGenerator[httpx.Request, httpx.Response]:
        await request.aread()
        self._check()
        sent: str | None = None
        for retry in (False, True):
            if retry or self._due():
                await self._aenter()
                try:
                    settled = not self._wanted(retry, sent)
                    while not settled:
                        delay = self._settle_delay()
                        if delay:
                            await self._async_sleep(delay)
                        refresh = self._presentation(request)
                        if self._transport is not None:
                            answer = await self._asend(refresh)
                        else:
                            try:
                                answer = yield refresh
                                await answer.aread()
                            except BaseException as error:
                                # As in `_sync_refresh`.
                                self._lost(error)
                                raise
                        settled = answer is not None and self._answered(answer)
                finally:
                    self._leave()
            sent = self._authorize(request)
            response = yield request
            if retry or not self._rejected(response):
                return
            await response.aread()
