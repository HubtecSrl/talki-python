"""`talki.oauth`: the consent URL and callback, the token
endpoints, and a `Talki` whose pair renews itself, over `httpx.MockTransport`."""

import asyncio
import base64
import json
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest

from talki import Talki
from talki.api.account import get_account
from talki.api.tags import create_tag
from talki.models import TagCreate
from talki.oauth import (
    OAuthApp,
    OAuthError,
    Pkce,
    TokenRefresh,
    TokenSet,
    authorization_url,
    read_callback,
)

BASIC = "Basic " + base64.b64encode(b"talki_cid_x:talki_cs_x").decode()


def pair(n: int, expires_in: int = 3600) -> dict:
    return {
        "access_token": f"talki_at_{n}",
        "token_type": "Bearer",
        "expires_in": expires_in,
        "refresh_token": f"talki_rt_{n}",
        "scope": "calls:read account:read",
        "account_id": "acc",
        "installation_id": "inst",
        "livemode": False,
    }


UNAUTHENTICATED = {
    "error": {
        "type": "authentication_error",
        "code": "invalid_credentials",
        "message": "The supplied API credential is invalid.",
        "request_id": "req_1",
    }
}
EXPIRED = httpx.Response(401, json=UNAUTHENTICATED, headers={"WWW-Authenticate": 'Bearer error="invalid_token"'})


class Server:
    """`/oauth/token` hands out pair n+1 for refresh token n; `/v1/account`
    accepts only the newest access token."""

    def __init__(self, *, fail_refresh: bool = False) -> None:
        self.current = 1
        self.fail_refresh = fail_refresh
        self.refreshes: list[str] = []
        self.api_tokens: list[str] = []
        self.lock = threading.Lock()

    def __call__(self, request: httpx.Request) -> httpx.Response:
        if request.url.path == "/oauth/token":
            form = parse_qs(request.content.decode())
            assert request.headers["Authorization"] == BASIC
            assert form["grant_type"] == ["refresh_token"]
            with self.lock:
                self.refreshes.append(form["refresh_token"][0])
                if self.fail_refresh or form["refresh_token"][0] != f"talki_rt_{self.current}":
                    return httpx.Response(400, json={"error": "invalid_grant", "error_description": "rotated"})
                self.current += 1
                return httpx.Response(200, json=pair(self.current))
        token = request.headers["Authorization"].removeprefix("Bearer ")
        self.api_tokens.append(token)
        if token != f"talki_at_{self.current}":
            return EXPIRED
        return httpx.Response(204)


def talki_with(server: Server, *, expires_at: float | None, saved: list[TokenSet] | None = None) -> Talki:
    transport = httpx.MockTransport(server)
    app = OAuthApp("talki_cid_x", "talki_cs_x", transport=transport)
    tokens = TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1", expires_at=expires_at)
    return Talki(
        tokens=tokens,
        oauth_app=app,
        on_token_refresh=(saved.append if saved is not None else None),
        transport=transport,
        max_retries=0,
    )


# The consent round trip.


def test_the_consent_url_carries_pkce_and_the_scopes():
    pkce = Pkce.new()
    url = authorization_url(
        "talki_cid_x",
        "https://crm.example/cb",
        ["calls:read", "account:read"],
        state="s1",
        pkce=pkce,
    )
    parts = urlsplit(url)
    query = {key: values[0] for key, values in parse_qs(parts.query).items()}
    assert f"{parts.scheme}://{parts.netloc}{parts.path}" == "https://app.talki.it/autorizza"
    assert query == {
        "response_type": "code",
        "client_id": "talki_cid_x",
        "redirect_uri": "https://crm.example/cb",
        "scope": "calls:read account:read",
        "state": "s1",
        "code_challenge": pkce.challenge,
        "code_challenge_method": "S256",
    }
    assert 43 <= len(pkce.verifier) <= 128


@pytest.mark.parametrize(
    ("callback", "error"),
    [
        (
            "https://crm.example/cb?error=access_denied&state=s1&iss=https://api.talki.it",
            "access_denied",
        ),
        ("https://crm.example/cb?code=c&state=other&iss=https://api.talki.it", "state_mismatch"),
        ("https://crm.example/cb?code=c&state=s1&iss=https://evil.example", "issuer_mismatch"),
        ("https://crm.example/cb?code=c&state=s1", "issuer_mismatch"),
        ("https://crm.example/cb?state=s1&iss=https://api.talki.it", "missing_code"),
    ],
    ids=["refused", "state", "issuer", "no-issuer", "no-code"],
)
def test_a_callback_that_is_not_a_code_for_this_request(callback, error):
    with pytest.raises(OAuthError) as raised:
        read_callback(callback, state="s1")
    assert raised.value.error == error


def test_a_good_callback_gives_its_code():
    assert read_callback("https://crm.example/cb?code=c1&state=s1&iss=https://api.talki.it", state="s1") == "c1"


def test_the_code_exchange():
    seen: list[httpx.Request] = []

    def token(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=pair(1))

    app = OAuthApp("talki_cid_x", "talki_cs_x", transport=httpx.MockTransport(token))
    tokens = app.exchange_code("c1", redirect_uri="https://crm.example/cb", code_verifier="v" * 64)
    assert seen[0].headers["Authorization"] == BASIC
    assert parse_qs(seen[0].content.decode()) == {
        "grant_type": ["authorization_code"],
        "code": ["c1"],
        "redirect_uri": ["https://crm.example/cb"],
        "code_verifier": ["v" * 64],
    }
    assert (tokens.access_token, tokens.refresh_token, tokens.scopes) == (
        "talki_at_1",
        "talki_rt_1",
        ("calls:read", "account:read"),
    )
    assert tokens.livemode is False
    assert "talki_at_1" not in repr(tokens) and "talki_cs_x" not in repr(app)


def test_a_refused_exchange_is_an_oauth_error():
    refused = httpx.Response(400, json={"error": "invalid_grant", "error_description": "spent"})
    app = OAuthApp("talki_cid_x", "talki_cs_x", transport=httpx.MockTransport(lambda request: refused))
    with pytest.raises(OAuthError) as raised:
        app.exchange_code("c1", redirect_uri="https://crm.example/cb", code_verifier="v" * 64)
    assert (raised.value.error, raised.value.status) == ("invalid_grant", 400)


# A pair that renews itself.


def test_a_401_invalid_token_renews_the_pair_once_and_retries():
    server = Server()
    saved: list[TokenSet] = []

    # The client's access token has expired; its refresh token is still live.
    def stale_access(request: httpx.Request) -> httpx.Response:
        if request.url.path != "/oauth/token" and request.headers["Authorization"] == "Bearer talki_at_1":
            server.api_tokens.append("talki_at_1")
            return EXPIRED
        return server(request)

    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1"),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", transport=httpx.MockTransport(stale_access)),
        on_token_refresh=saved.append,
        transport=httpx.MockTransport(stale_access),
        max_retries=0,
    )
    with talki:
        response = get_account.sync_detailed(client=talki.client)
    assert response.status_code == 204
    assert server.refreshes == ["talki_rt_1"]
    assert server.api_tokens == ["talki_at_1", "talki_at_2"]
    assert [tokens.refresh_token for tokens in saved] == ["talki_rt_2"]
    assert talki.tokens is not None and talki.tokens.access_token == "talki_at_2"


def test_a_pair_about_to_expire_is_renewed_before_the_request():
    server = Server()
    saved: list[TokenSet] = []
    talki = talki_with(server, expires_at=0.0, saved=saved)
    with talki:
        # talki_at_1 is still accepted: the renewal is driven by expires_at alone.
        get_account.sync_detailed(client=talki.client)
    assert server.refreshes == ["talki_rt_1"]
    assert server.api_tokens == ["talki_at_2"]
    assert len(saved) == 1


def test_a_401_without_invalid_token_is_left_alone():
    refused = httpx.Response(401, json=UNAUTHENTICATED)
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        return refused

    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1"),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_x"),
        transport=httpx.MockTransport(handler),
    )
    with talki:
        assert get_account.sync_detailed(client=talki.client).status_code == 401
    assert calls == ["/v1/account"]


def test_a_refused_refresh_raises_and_keeps_the_old_pair():
    server = Server(fail_refresh=True)
    talki = talki_with(server, expires_at=0.0)
    with talki:
        with pytest.raises(OAuthError) as raised:
            get_account.sync_detailed(client=talki.client)
    assert raised.value.error == "invalid_grant"
    assert talki.tokens is not None and talki.tokens.refresh_token == "talki_rt_1"


def test_a_pair_that_cannot_be_stored_is_not_used():
    server = Server()

    def cannot_store(tokens: TokenSet) -> None:
        raise OSError("disk full")

    transport = httpx.MockTransport(server)
    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1", expires_at=0.0),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", transport=transport),
        on_token_refresh=cannot_store,
        transport=transport,
    )
    with talki:
        with pytest.raises(OSError):
            get_account.sync_detailed(client=talki.client)
    assert talki.tokens is not None and talki.tokens.access_token == "talki_at_1"
    assert server.api_tokens == []


def test_threads_sharing_an_expired_pair_renew_it_once():
    server = Server()
    talki = talki_with(server, expires_at=0.0)
    with talki:
        with ThreadPoolExecutor(max_workers=8) as pool:
            statuses = list(pool.map(lambda _: get_account.sync_detailed(client=talki.client).status_code, range(16)))
    assert statuses == [204] * 16
    assert server.refreshes == ["talki_rt_1"]


def test_the_async_client_renews_too():
    server = Server()
    saved: list[TokenSet] = []
    talki = talki_with(server, expires_at=0.0, saved=saved)

    async def run() -> int:
        async with talki:
            response = await get_account.asyncio_detailed(client=talki.client)
        return int(response.status_code)

    assert asyncio.run(run()) == 204
    assert server.refreshes == ["talki_rt_1"]
    assert len(saved) == 1


def test_oauth_app_needs_tokens():
    with pytest.raises(ValueError):
        Talki(access_token="talki_at_1", oauth_app=OAuthApp("talki_cid_x", "talki_cs_x"))


def test_on_token_refresh_needs_oauth_app():
    """Without the app nothing renews, so the callback would never be called."""
    with pytest.raises(ValueError, match="oauth_app"):
        Talki(
            tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1"),
            on_token_refresh=lambda tokens: None,
        )


# The review's edge cases.


def test_the_refresh_inherits_the_requests_timeout_and_is_retried_only_unsent():
    seen: list[httpx.Request] = []
    server = Server()

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return server(request)

    transport = httpx.MockTransport(handler)
    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1", expires_at=0.0),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", transport=transport),
        transport=transport,
        timeout=7.0,
    )
    with talki:
        get_account.sync_detailed(client=talki.client)
    refresh = seen[0]
    assert refresh.url.path == "/oauth/token"
    assert refresh.extensions["timeout"]["read"] == 7.0
    assert refresh.extensions["talki.unsent_only"] is True


def test_a_pair_that_could_not_be_stored_is_stored_before_anything_else():
    server = Server()
    attempts: list[TokenSet] = []

    def store(tokens: TokenSet) -> None:
        attempts.append(tokens)
        if len(attempts) == 1:
            raise OSError("disk full")

    transport = httpx.MockTransport(server)
    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1", expires_at=0.0),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", transport=transport),
        on_token_refresh=store,
        transport=transport,
    )
    with talki:
        with pytest.raises(OSError):
            get_account.sync_detailed(client=talki.client)
        assert get_account.sync_detailed(client=talki.client).status_code == 204
    # One refresh: the pending pair was stored, never re-requested with talki_rt_1.
    assert server.refreshes == ["talki_rt_1"]
    assert [tokens.refresh_token for tokens in attempts] == ["talki_rt_2", "talki_rt_2"]
    assert server.api_tokens == ["talki_at_2"]


def test_a_revoked_installation_fails_fast_after_the_first_refusal():
    server = Server(fail_refresh=True)
    talki = talki_with(server, expires_at=0.0)
    with talki:
        for _ in range(3):
            with pytest.raises(OAuthError):
                get_account.sync_detailed(client=talki.client)
    assert server.refreshes == ["talki_rt_1"]


def test_a_write_answered_401_is_sent_again_with_its_body():
    server = Server()
    bodies: list[bytes] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/tags":
            bodies.append(request.content)
            if request.headers["Authorization"] == "Bearer talki_at_1":
                return EXPIRED
            return httpx.Response(204)
        return server(request)

    transport = httpx.MockTransport(handler)
    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1"),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", transport=transport),
        transport=transport,
    )
    with talki:
        create_tag.sync_detailed(client=talki.client, body=TagCreate(name="VIP", color="#e0867a"))
    assert len(bodies) == 2 and bodies[0] == bodies[1] and json.loads(bodies[0])["name"] == "VIP"


def test_a_second_401_is_returned_not_looped():
    server = Server()

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/oauth/token":
            return server(request)
        return EXPIRED

    transport = httpx.MockTransport(handler)
    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1"),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", transport=transport),
        transport=transport,
    )
    with talki:
        assert get_account.sync_detailed(client=talki.client).status_code == 401
    assert server.refreshes == ["talki_rt_1"]


def test_sync_and_async_calls_share_one_renewal():
    server = Server()
    talki = talki_with(server, expires_at=0.0)

    async def many() -> list[int]:
        async with talki:
            answers = await asyncio.gather(*(get_account.asyncio_detailed(client=talki.client) for _ in range(10)))
        return [int(answer.status_code) for answer in answers]

    with talki:
        assert get_account.sync_detailed(client=talki.client).status_code == 204
    assert asyncio.run(many()) == [204] * 10
    assert server.refreshes == ["talki_rt_1"]


def test_waiting_threads_do_not_hold_the_pool():
    """A real server, two pooled connections, eight threads whose token is
    refused: the renewal still gets a connection, and every call ends."""
    state = {"current": 1, "refreshes": 0}
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _send(self, status: int, body: dict, headers: dict[str, str] | None = None) -> None:
            raw = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            for key, value in (headers or {}).items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(raw)

        def do_POST(self):
            self.rfile.read(int(self.headers["Content-Length"]))
            with lock:
                state["refreshes"] += 1
                state["current"] += 1
                self._send(200, pair(state["current"]))

        def do_GET(self):
            time.sleep(0.05)
            if self.headers["Authorization"] != f"Bearer talki_at_{state['current']}":
                self._send(401, UNAUTHENTICATED, {"WWW-Authenticate": 'Bearer error="invalid_token"'})
            else:
                self._send(200, {"ok": True})

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    try:
        limited = httpx.HTTPTransport(limits=httpx.Limits(max_connections=2))
        talki = Talki(
            tokens=TokenSet(access_token="talki_at_0", refresh_token="talki_rt_0"),
            oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", base_url=base),
            base_url=base,
            transport=limited,
            timeout=5.0,
        )
        talki.auth._app._transport = limited
        with talki, ThreadPoolExecutor(max_workers=8) as pool:
            client = talki.client.get_httpx_client()
            statuses = list(pool.map(lambda _: client.get("/v1/account").status_code, range(8)))
        assert statuses == [200] * 8
        assert state["refreshes"] == 1
    finally:
        httpd.shutdown()


def test_more_of_the_app_surface():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path == "/oauth/revoke":
            return httpx.Response(200)
        body = pair(2)
        del body["expires_in"]
        return httpx.Response(200, json=body)

    app = OAuthApp("talki_cid_x", "talki_cs_x", transport=httpx.MockTransport(handler))
    tokens = app.refresh("talki_rt_1", scopes=["calls:read"])
    assert tokens.expires_at is None
    assert parse_qs(seen[0].content.decode())["scope"] == ["calls:read"]
    app.revoke("talki_rt_2")
    assert parse_qs(seen[1].content.decode()) == {"token": ["talki_rt_2"]}


def test_callback_edges():
    assert read_callback("?code=c1&state=s1&iss=https://api.talki.it", state="s1") == "c1"
    with pytest.raises(OAuthError):
        read_callback("https://crm.example/cb?code=c&state=é&iss=https://api.talki.it", state="s1")
    with pytest.raises(ValueError):
        read_callback("https://crm.example/cb?code=c&iss=https://api.talki.it", state="")
    assert "verifier=" not in repr(Pkce.new())


def test_a_pair_is_renewed_where_it_was_issued():
    with pytest.raises(ValueError):
        Talki(
            tokens=TokenSet(access_token="a", refresh_token="r"),
            oauth_app=OAuthApp("talki_cid_x", "talki_cs_x"),
            base_url="https://api.sandbox.example",
        )


def test_calling_the_same_talki_from_on_token_refresh_raises_instead_of_hanging():
    server = Server()
    holder: list[Talki] = []

    def store(tokens: TokenSet) -> None:
        get_account.sync_detailed(client=holder[0].client)

    transport = httpx.MockTransport(server)
    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1", expires_at=0.0),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", transport=transport),
        on_token_refresh=store,
        transport=transport,
    )
    holder.append(talki)
    with talki:
        with pytest.raises(RuntimeError):
            get_account.sync_detailed(client=talki.client)


def test_wrong_app_credentials_are_asked_about_once_and_each_failure_is_fresh():
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        return httpx.Response(401, json={"error": "invalid_client", "error_description": "wrong secret"})

    transport = httpx.MockTransport(handler)
    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1", expires_at=0.0),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_wrong", transport=transport),
        transport=transport,
    )
    raised = []
    with talki:
        for _ in range(3):
            with pytest.raises(OAuthError) as error:
                get_account.sync_detailed(client=talki.client)
            raised.append(error.value)
    assert calls == ["/oauth/token"]
    assert {error.error for error in raised} == {"invalid_client"}
    assert raised[1] is not raised[2]


def test_a_pending_pair_is_stored_by_the_next_request_never_refreshed_again():
    server = Server()
    failures = [OSError("disk full")]

    def store(tokens: TokenSet) -> None:
        if failures:
            raise failures.pop()

    transport = httpx.MockTransport(server)
    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1", expires_at=0.0),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", transport=transport),
        on_token_refresh=store,
        transport=transport,
    )
    with talki:
        with pytest.raises(OSError):
            get_account.sync_detailed(client=talki.client)
        assert get_account.sync_detailed(client=talki.client).status_code == 204
    assert server.refreshes == ["talki_rt_1"]
    assert server.api_tokens == ["talki_at_2"]


# A refresh whose outcome is unknown. The server takes the same refresh token
# once more within 60 s of its first rotation; an overlap, or a presentation
# after that, revokes the installation.


class Wire:
    """The token endpoint answers refreshes in turn from ``script`` (then with
    pair 2): an answer, an exception, or ``(seconds, either)`` for one that
    ends that long after it was sent. ``now`` is the refresher's clock, moved
    only by the script and its waits; ``timeline`` logs both."""

    def __init__(self, *script: object) -> None:
        self.script = list(script)
        self.now = 1000.0
        self.timeline: list[str] = []
        self.transport_waits: list[float] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        if request.url.path != "/oauth/token":
            self.timeline.append("GET")
            return httpx.Response(204)
        assert parse_qs(request.content.decode())["refresh_token"] == ["talki_rt_1"]
        self.timeline.append(f"refresh at {self.now:g}")
        step = self.script.pop(0) if self.script else httpx.Response(200, json=pair(2))
        if isinstance(step, tuple):
            seconds, step = step
            self.now += seconds
        if isinstance(step, BaseException):
            raise step
        assert isinstance(step, httpx.Response)
        return step

    def wait(self, delay: float) -> None:
        self.timeline.append(f"wait {delay:g}")
        self.now += delay

    async def async_wait(self, delay: float) -> None:
        self.wait(delay)

    def watch(self, auth: TokenRefresh) -> None:
        auth._monotonic = lambda: self.now
        auth._sleep = self.wait
        auth._async_sleep = self.async_wait

    def talki(self) -> Talki:
        transport = httpx.MockTransport(self)
        talki = Talki(
            tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1", expires_at=0.0),
            oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", transport=transport),
            transport=transport,
        )
        assert talki.auth is not None
        self.watch(talki.auth)
        talki.transport._sleep = self.transport_waits.append

        async def transport_wait(delay: float) -> None:
            self.transport_waits.append(delay)

        talki.transport._async_sleep = transport_wait
        return talki


def call(talki: Talki, mode: str) -> int:
    if mode == "sync":
        return int(get_account.sync_detailed(client=talki.client).status_code)

    async def run() -> int:
        return int((await get_account.asyncio_detailed(client=talki.client)).status_code)

    return asyncio.run(run())


MODES = pytest.mark.parametrize("mode", ["sync", "async"])
GATEWAY = httpx.Response(502, text="<html>502 Bad Gateway</html>")


@MODES
def test_a_refresh_whose_connection_broke_is_presented_again_after_the_settle(mode):
    """Not by the transport a moment later, which could overlap the first
    still running on the server: the request waits, then asks again."""
    wire = Wire(httpx.ReadError("connection dropped after sending"))
    talki = wire.talki()
    assert call(talki, mode) == 204
    assert wire.timeline == ["refresh at 1000", "wait 10", "refresh at 1010", "GET"]
    assert wire.transport_waits == []
    assert talki.tokens is not None and talki.tokens.refresh_token == "talki_rt_2"


@MODES
def test_a_refresh_that_timed_out_is_presented_again_within_the_grace(mode):
    """The wait is timed from the timeout, not from the send."""
    wire = Wire((30.0, httpx.ReadTimeout("slow")))
    assert call(wire.talki(), mode) == 204
    assert wire.timeline == ["refresh at 1000", "wait 10", "refresh at 1040", "GET"]


@MODES
def test_a_timeout_too_late_for_the_grace_raises_and_the_next_request_waits(mode):
    wire = Wire((50.0, httpx.ReadTimeout("slow")))
    talki = wire.talki()
    with pytest.raises(httpx.ReadTimeout):
        call(talki, mode)
    wire.now += 4.0
    assert call(talki, mode) == 204
    assert wire.timeline == ["refresh at 1000", "wait 6", "refresh at 1060", "GET"]


@MODES
def test_a_gateway_failure_on_a_refresh_is_an_unknown_outcome(mode):
    """The app may have rotated the pair, then died before answering."""
    wire = Wire(GATEWAY)
    assert call(wire.talki(), mode) == 204
    assert wire.timeline == ["refresh at 1000", "wait 10", "refresh at 1010", "GET"]
    assert wire.transport_waits == []


def test_gateway_failures_past_the_grace_raise_and_leave_the_next_request_waiting():
    wire = Wire(*[GATEWAY] * 6)
    talki = wire.talki()
    with pytest.raises(OAuthError) as error:
        call(talki, "sync")
    assert error.value.status == 502
    presented = [entry for entry in wire.timeline if entry.startswith("refresh")]
    assert presented == [f"refresh at {at}" for at in (1000, 1010, 1020, 1030, 1040, 1050)]
    wire.now += 1.0
    assert call(talki, "sync") == 204
    assert wire.timeline[-3:] == ["wait 9", "refresh at 1060", "GET"]


@MODES
def test_a_refresh_that_never_connected_is_retried_at_once_and_leaves_no_doubt(mode):
    wire = Wire(*[httpx.ConnectError("refused")] * 3)
    talki = wire.talki()
    with pytest.raises(httpx.ConnectError):
        call(talki, mode)
    assert len(wire.transport_waits) == 2
    assert call(talki, mode) == 204
    assert wire.timeline == ["refresh at 1000"] * 4 + ["GET"]


class Abandoned(BaseException):
    """Like a cancellation or an interrupt: no one waits for the answer."""


def test_an_abandoned_refresh_is_not_retried_and_the_next_one_waits():
    wire = Wire(Abandoned())
    talki = wire.talki()
    with pytest.raises(Abandoned):
        call(talki, "sync")
    wire.now += 3.0
    assert call(talki, "sync") == 204
    assert wire.timeline == ["refresh at 1000", "wait 7", "refresh at 1010", "GET"]


def test_without_the_transport_a_lost_answer_waits_for_the_next_request():
    """Through httpx's own send, a failure closes the flow without saying
    which: assumed to have reached the server."""
    wire = Wire(httpx.ConnectError("refused"))
    transport = httpx.MockTransport(wire)
    auth = TokenRefresh(
        TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1", expires_at=0.0),
        OAuthApp("talki_cid_x", "talki_cs_x", transport=transport),
    )
    wire.watch(auth)
    with httpx.Client(base_url="https://api.talki.it", transport=transport, auth=auth) as client:
        with pytest.raises(httpx.ConnectError):
            client.get("/v1/account")
        assert client.get("/v1/account").status_code == 204
    assert wire.timeline == ["refresh at 1000", "wait 10", "refresh at 1010", "GET"]


def test_async_waiters_are_woken_by_a_renewal_in_another_thread():
    """Without polling: the release wakes them."""
    started, finish = threading.Event(), threading.Event()
    server = Server()

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/oauth/token":
            started.set()
            assert finish.wait(5)
        return server(request)

    transport = httpx.MockTransport(handler)
    talki = Talki(
        tokens=TokenSet(access_token="talki_at_1", refresh_token="talki_rt_1", expires_at=0.0),
        oauth_app=OAuthApp("talki_cid_x", "talki_cs_x", transport=transport),
        transport=transport,
    )
    assert talki.auth is not None
    polls: list[float] = []

    async def poll(delay: float) -> None:
        polls.append(delay)

    talki.auth._async_sleep = poll
    renewal = threading.Thread(target=lambda: get_account.sync_detailed(client=talki.client))
    renewal.start()
    assert started.wait(5)

    async def waiters() -> list[int]:
        calls = asyncio.gather(*(get_account.asyncio_detailed(client=talki.client) for _ in range(5)))
        await asyncio.sleep(0.05)
        finish.set()
        return [int(answer.status_code) for answer in await asyncio.wait_for(calls, 5)]

    assert asyncio.run(waiters()) == [204] * 5
    renewal.join(5)
    assert server.refreshes == ["talki_rt_1"]
    assert polls == []


def test_a_renewal_is_logged_and_no_token_is(caplog):
    server = Server()
    with caplog.at_level(logging.INFO, logger="talki"):
        with talki_with(server, expires_at=0.0) as talki:
            get_account.sync_detailed(client=talki.client)
    assert [record.getMessage() for record in caplog.records if record.name == "talki.oauth"] == [
        "Renewed the access token of installation inst."
    ]
    assert "talki_at_" not in caplog.text and "talki_rt_" not in caplog.text and "talki_cs_" not in caplog.text


def test_a_refused_renewal_is_logged_as_an_error(caplog):
    with caplog.at_level(logging.INFO, logger="talki"):
        with talki_with(Server(fail_refresh=True), expires_at=0.0) as talki:
            with pytest.raises(OAuthError):
                get_account.sync_detailed(client=talki.client)
    (record,) = [record for record in caplog.records if record.name == "talki.oauth"]
    assert record.levelno == logging.ERROR
    assert record.getMessage() == (
        "The API refused the token renewal (invalid_grant): the customer has to reconnect the app"
    )
