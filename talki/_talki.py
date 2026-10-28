"""`Talki` and `AsyncTalki`, the clients to start from.

    from talki import Talki

    with Talki(api_key="talki_test_…") as talki:
        account = talki.account.get()
        for call in talki.calls.list(limit=100):
            ...

`AsyncTalki` takes the same arguments, and its methods are awaited:
`account = await talki.account.get()`. Each method returns the operation's
value or raises the `talki.ApiError` subclass for its error.

`talki.with_options(timeout=…, max_retries=…)` is the same client with other
settings, for the calls made on it. `talki.<tag>.with_raw_response` has the
same methods, returning the whole answer (`ETag`, `X-Request-Id`, …) with the
value.

`talki.client` is the generated `AuthenticatedClient`, for the operations under
`talki.api`: `get_account.sync_detailed(client=talki.client)`, then `unwrap` it.
"""

from __future__ import annotations

import os
import ssl
from collections.abc import Callable
from types import TracebackType
from typing import Self

import httpx

from ._resource import unwrap
from ._transport import TalkiTransport
from ._version import USER_AGENT
from .api import AsyncResources, Resources
from .client import AuthenticatedClient
from .oauth import OAuthApp, TokenRefresh, TokenSet

__all__ = ["DEFAULT_BASE_URL", "AsyncTalki", "Talki", "unwrap"]

DEFAULT_BASE_URL = "https://api.talki.it"
VERSION_HEADER = "Talki-Version"
# Read for `api_key` when no credential is passed.
API_KEY_ENV = "TALKI_API_KEY"


class _Current:
    def __repr__(self) -> str:
        return "API_VERSION"


# `version`'s default: `talki.API_VERSION`, read when a client is built.
CURRENT = _Current()


class _Configured:
    """What `Talki` and `AsyncTalki` share: the credentials, the transport and
    the generated `client`."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        access_token: str | None = None,
        tokens: TokenSet | None = None,
        oauth_app: OAuthApp | None = None,
        on_token_refresh: Callable[[TokenSet], None] | None = None,
        version: str | None | _Current = CURRENT,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 2,
        auto_idempotency: bool = True,
        verify: ssl.SSLContext | str | bool = True,
        proxy: str | None = None,
        transport: httpx.BaseTransport | httpx.AsyncBaseTransport | None = None,
        user_agent: str | None = None,
    ) -> None:
        """A client for Talki's public API.

        Args:
            api_key: A business's API key (`talki_live_…`, or `talki_test_…` for a
                sandbox). With no credential passed at all, it is read from the
                `TALKI_API_KEY` environment variable.
            access_token: An OAuth installation's access token (`talki_at_…`), when
                not using an API key.
            tokens: An installation's whole pair (`talki.oauth.TokenSet`), instead of
                ``access_token``. With ``oauth_app`` the pair renews itself: before
                it expires, and when the API answers that it has. Exactly one of
                ``api_key``, ``access_token`` and ``tokens`` is required.
            oauth_app: The app's credentials (`talki.oauth.OAuthApp`), to renew
                ``tokens``.
            on_token_refresh: Called with each new pair, before it is used: store
                it there. The previous refresh token stops working. Only with
                ``oauth_app``.
            version: The `Talki-Version` sent on every request. Defaults to
                `talki.API_VERSION`, the contract this package was generated from;
                None sends none, and the version pinned on the key or app applies.
            base_url: The API's origin.
            timeout: Seconds before a request is abandoned.
            max_retries: How often a failed request is tried again; 0 for never.
                See `talki._transport` for what is retried. `timeout` applies to
                each attempt.
            auto_idempotency: Give every write without an `Idempotency-Key` a new
                one. Pass `idempotency_key=` to an operation to choose your own,
                for instance to retry a write across process restarts.
            verify: TLS verification, as httpx takes it.
            proxy: A proxy URL for every request. Proxy environment variables
                (`HTTPS_PROXY`, …) are not read.
            transport: The httpx transport requests go out on, for tests
                (`httpx.MockTransport`); httpx's own by default. It is closed with
                the client, and must take requests again after that.
            user_agent: Your product and version (`acme-crm/2.1`), added after
                this package's own in the `User-Agent` of every API request. A
                token renewal carries this package's alone, as `OAuthApp` sends it.
        """
        if api_key is None and access_token is None and tokens is None:
            api_key = os.environ.get(API_KEY_ENV, "").strip() or None
        given = [value for value in (api_key, access_token, tokens) if value is not None]
        if len(given) != 1:
            raise ValueError(f"Pass exactly one of api_key, access_token and tokens, or set {API_KEY_ENV}.")
        if oauth_app is not None and tokens is None:
            raise ValueError("oauth_app renews tokens: pass tokens too.")
        if on_token_refresh is not None and oauth_app is None:
            raise ValueError("on_token_refresh is called when tokens renew, which takes oauth_app: pass it too.")
        if oauth_app is not None and oauth_app.base_url != base_url.rstrip("/"):
            # A staging pair renewed against production would send the refresh
            # token and the client secret to the wrong deployment.
            raise ValueError(f"oauth_app talks to {oauth_app.base_url}, this client to {base_url}: make them the same.")
        if user_agent is not None and (
            not user_agent.strip() or not user_agent.isascii() or not user_agent.isprintable()
        ):
            raise ValueError("user_agent must be one non-blank line of printable ASCII.")
        token = tokens.access_token if tokens is not None else str(given[0])
        if isinstance(version, _Current):
            from . import API_VERSION

            version = API_VERSION
        self.version = version
        self._tokens = tokens
        self.base_url = base_url.rstrip("/")
        self.transport = TalkiTransport(
            max_retries=max_retries,
            auto_idempotency=auto_idempotency,
            verify=verify,
            proxy=proxy,
            transport=transport,
        )
        self.auth = (
            TokenRefresh(tokens, oauth_app, on_refresh=on_token_refresh, transport=self.transport)
            if tokens and oauth_app
            else None
        )
        self._token = token
        self._verify = verify
        self._headers = {
            "User-Agent": f"{USER_AGENT} {user_agent.strip()}" if user_agent else USER_AGENT,
            **({VERSION_HEADER: version} if version else {}),
        }
        self.timeout = timeout
        self.client = self._client_for(self.transport, timeout)
        # False on a `with_options` copy, whose connections are its original's.
        self._owns_connections = True

    def _client_for(self, transport: TalkiTransport, timeout: float) -> AuthenticatedClient:
        return AuthenticatedClient(
            base_url=self.base_url,
            token=self._token,
            headers=dict(self._headers),
            timeout=httpx.Timeout(timeout),
            verify_ssl=self._verify,
            httpx_args={"transport": transport, **({"auth": self.auth} if self.auth else {})},
        )

    def with_options(self, *, timeout: float | None = None, max_retries: int | None = None) -> Self:
        """This client with another ``timeout`` or ``max_retries``, for the
        calls made on what it returns: `talki.with_options(timeout=5).calls.get(id)`.

        The copy shares this client's connections and its token renewal, so it
        is cheap to make for one call. They belong to this client: closing the
        copy (or leaving its ``with`` block) leaves them open, and closing this
        client closes them for both, which stay usable, as after any `close`.
        """
        copy = object.__new__(type(self))
        # Every attribute but the per-tag resources, which are bound to the
        # old `client` and built again on first use.
        copy.__dict__.update({name: value for name, value in vars(self).items() if name in _SETTINGS})
        if max_retries is not None:
            copy.transport = self.transport.with_retries(max_retries)
        if timeout is not None:
            copy.timeout = timeout
        copy.client = copy._client_for(copy.transport, copy.timeout)
        copy._owns_connections = False
        return copy

    @property
    def tokens(self) -> TokenSet | None:
        """The current pair, when built with ``tokens`` (renewed in place)."""
        return self.auth.tokens if self.auth is not None else self._tokens

    def __repr__(self) -> str:
        # Never the credential.
        return f"{type(self).__name__}(base_url={self.base_url!r}, version={self.version!r})"


# What `with_options` copies: everything `_Configured.__init__` sets.
_SETTINGS = frozenset(
    {"version", "_tokens", "base_url", "transport", "auth", "_token", "_verify", "_headers", "timeout", "client"}
)
# Set by `__init__` and `with_options` each for itself.
_OWN = frozenset({"_owns_connections"})


class Talki(_Configured, Resources):
    """A client for Talki's public API, whose methods are sync:
    `talki.calls.list()`. Use `AsyncTalki` in async code.

    Open it with ``with`` to close its connections at the end of the block, or
    keep one for the life of the process and call `close` when done.
    """

    def close(self) -> None:
        """Close the connections the sync methods opened. The client stays
        usable: the next request opens new ones. Call it with no request in
        flight: one running on another thread may fail. On a `with_options`
        copy, it leaves the connections to the client it came from."""
        _close(self.client, self._owns_connections)

    async def aclose(self) -> None:
        """Close the connections the async operations under `talki.api` opened."""
        await _aclose(self.client, self._owns_connections)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    # For the async operations under `talki.api`, sent with `client`: the
    # methods of `talki.calls` and the others are sync here, async on
    # `AsyncTalki`.
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()


class AsyncTalki(_Configured, AsyncResources):
    """A client for Talki's public API, whose methods are awaited:
    `await talki.calls.list()`. It takes the same arguments as `Talki`.

    Open it with ``async with`` to close its connections at the end of the
    block, or keep one for the life of the process and await `aclose` when done.
    """

    async def aclose(self) -> None:
        """Close the connections the methods opened. The client stays usable:
        the next request opens new ones. Call it with no request in flight:
        one running on another task may fail. On a `with_options` copy, it
        leaves the connections to the client it came from."""
        await _aclose(self.client, self._owns_connections)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()


# The generated client builds its httpx clients on first use and keeps them in
# `_client` / `_async_client`. A closed httpx client cannot be opened again, so
# closing drops it, and the next request builds a new one. Closing an httpx
# client closes its transport's connections: a copy that does not own them
# only drops its client, which holds nothing else.
def _close(client: AuthenticatedClient, owns_connections: bool) -> None:
    opened, client._client = client._client, None
    if opened is not None and owns_connections:
        opened.close()


async def _aclose(client: AuthenticatedClient, owns_connections: bool) -> None:
    opened, client._async_client = client._async_client, None
    if opened is not None and owns_connections:
        await opened.aclose()
