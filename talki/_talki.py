"""`Talki`, the client to start from, and `unwrap`, which turns an answer into
its value or an exception.

    from talki import Talki, unwrap
    from talki.api.account import get_account

    with Talki(api_key="talki_test_…") as talki:
        account = unwrap(get_account.sync_detailed(client=talki.client))

`talki.client` is the generated `AuthenticatedClient`, so every operation under
`talki.api` takes it, sync or async (`async with Talki(…)`).
"""

from __future__ import annotations

import ssl
from collections.abc import Callable
from types import TracebackType
from typing import Any, TypeVar, cast

import httpx

from ._transport import TalkiTransport
from .client import AuthenticatedClient
from .exceptions import ApiError, error_from
from .models import ErrorEnvelope
from .oauth import OAuthApp, TokenRefresh, TokenSet
from .types import Response

__all__ = ["DEFAULT_BASE_URL", "Talki", "unwrap"]

T = TypeVar("T")

DEFAULT_BASE_URL = "https://api.talki.it"
VERSION_HEADER = "Talki-Version"


class _Current:
    def __repr__(self) -> str:
        return "API_VERSION"


# `version`'s default: `talki.API_VERSION`, read when a client is built.
CURRENT = _Current()


class Talki:
    """A configured client for Talki's public API.

    Args:
        api_key: A business's API key (`talki_live_…`, or `talki_test_…` for a
            sandbox).
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
            (`httpx.MockTransport`); httpx's own by default.
    """

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
    ) -> None:
        given = [value for value in (api_key, access_token, tokens) if value is not None]
        if len(given) != 1:
            raise ValueError("Pass exactly one of api_key, access_token and tokens.")
        if oauth_app is not None and tokens is None:
            raise ValueError("oauth_app renews tokens: pass tokens too.")
        if on_token_refresh is not None and oauth_app is None:
            raise ValueError("on_token_refresh is called when tokens renew, which takes oauth_app: pass it too.")
        if oauth_app is not None and oauth_app.base_url != base_url.rstrip("/"):
            # A staging pair renewed against production would send the refresh
            # token and the client secret to the wrong deployment.
            raise ValueError(f"oauth_app talks to {oauth_app.base_url}, this client to {base_url}: make them the same.")
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
        self.client = AuthenticatedClient(
            base_url=self.base_url,
            token=token,
            headers={VERSION_HEADER: version} if version else {},
            timeout=httpx.Timeout(timeout),
            verify_ssl=verify,
            httpx_args={"transport": self.transport, **({"auth": self.auth} if self.auth else {})},
        )

    @property
    def tokens(self) -> TokenSet | None:
        """The current pair, when built with ``tokens`` (renewed in place)."""
        return self.auth.tokens if self.auth is not None else self._tokens

    def __repr__(self) -> str:
        # Never the credential.
        return f"Talki(base_url={self.base_url!r}, version={self.version!r})"

    def __enter__(self) -> Talki:
        self.client.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.client.__exit__(exc_type, exc, traceback)

    async def __aenter__(self) -> Talki:
        await self.client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.client.__aexit__(exc_type, exc, traceback)


def unwrap(response: Response[T | ErrorEnvelope]) -> T:
    """The value of a `*_detailed` answer, or the `ApiError` subclass for its
    error.

    Returns None for a `204 No Content`. Raises for an error envelope, any
    status of 400 or more, and a success whose body this client could not read
    (a status the operation does not declare).
    """
    status = int(response.status_code)
    parsed: Any = response.parsed
    if status >= 400 or isinstance(parsed, ErrorEnvelope):
        raise error_from(status, response.headers, response.content)
    if parsed is None and response.content:
        raise ApiError(
            status=status,
            message="The answer has a status this operation does not declare.",
            headers=response.headers,
            body=response.content,
        )
    return cast(T, parsed)
