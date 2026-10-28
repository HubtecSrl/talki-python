"""The httpx transport `Talki` sends every request through: it adds an
`Idempotency-Key` to a write that has none, and retries what is safe to retry.

One object serves the sync and the async client alike, because
`AuthenticatedClient` hands the same settings to both.

Retried, at most `max_retries` times:
* any request that never left (connection refused, connect or pool timeout);
* any request answered 429 or `409 request_in_progress`: the API turned it
  away before running it;
* a `GET`, `HEAD` or `OPTIONS` answered 500, 502, 503 or 504, or whose
  connection broke after sending;
* a write carrying an `Idempotency-Key` answered 502, 503 or 504 by a gateway
  (a body that is not the API's error envelope). The API answers a repeated
  key with the first answer, or `request_in_progress` while that one runs.

Never retried: a write answered 5xx by the API itself, or whose connection
broke after sending, since either may come after the write was saved. Its key
keeps a repeat from applying it twice: the API answers the key of a write that
saved and then failed with that same 500 for 24 hours, and releases a key only
when nothing was saved. Read the resource to learn which happened; to retry,
use the key sent, which is on the exception
(`error.request.headers["Idempotency-Key"]` for an httpx error).

A request carrying `UNSENT_ONLY` (a token refresh) is retried only when it
never left, or was turned away unrun (429, `request_in_progress`): once it may
have reached the API, the one who sent it decides when to send it again.

The wait is the answer's `Retry-After` when it gives one, else exponential
backoff with jitter. An answer asking for more than `MAX_RETRY_AFTER` seconds
is returned as is, for the caller to schedule.
"""

from __future__ import annotations

import json
import logging
import random
import ssl
import threading
import time
import uuid
from collections.abc import Awaitable, Callable

import anyio
import httpx

from .exceptions import REQUEST_ID_HEADER, retry_after_seconds

# Under the `talki` logger. A request is logged by method and path, never its
# query (`phone=`, `q=`) or headers, so no credential or caller's data reaches
# a log.
logger = logging.getLogger(__name__)

IDEMPOTENCY_HEADER = "Idempotency-Key"
# A request extension: retry this only when it never left, or was turned away
# unrun. Its sender repeats it, if at all, once it may have arrived: a token
# refresh, whose repeat must wait for the first to finish on the server.
UNSENT_ONLY = "talki.unsent_only"
WRITE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})
SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})
SAFE_RETRY_STATUSES = frozenset({500, 502, 503, 504})
GATEWAY_STATUSES = frozenset({502, 503, 504})
MAX_RETRY_AFTER = 60.0
BACKOFF_BASE = 0.5
BACKOFF_CAP = 8.0

# Never sent: retrying cannot apply the request twice.
NOT_SENT = (httpx.ConnectError, httpx.ConnectTimeout, httpx.PoolTimeout)
# Possibly sent: retried for reads only.
_MAYBE_SENT = (httpx.ReadTimeout, httpx.WriteTimeout, httpx.ReadError, httpx.WriteError, httpx.RemoteProtocolError)


def new_idempotency_key() -> str:
    """A fresh `Idempotency-Key`: keep it to send a write again as the same one."""
    return str(uuid.uuid4())


def _key(request: httpx.Request) -> str:
    return str(request.headers.get(IDEMPOTENCY_HEADER, "")).strip()


def _envelope_code(response: httpx.Response, body: bytes | None) -> str | None:
    """The `error.code` of an answer whose ``body`` was read here, or None when
    it is not the API's JSON envelope."""
    if body is None or "json" not in response.headers.get("content-type", ""):
        return None
    try:
        detail = json.loads(body).get("error")
    except (ValueError, AttributeError):
        return None
    if not isinstance(detail, dict):
        return None
    code = detail.get("code")
    return code if isinstance(code, str) else ""


class _Connections:
    """The httpx transports requests go out on, opened on first use: what a
    `TalkiTransport` and its `with_retries` copies share."""

    def __init__(
        self,
        verify: ssl.SSLContext | str | bool,
        proxy: str | None,
        transport: httpx.BaseTransport | httpx.AsyncBaseTransport | None,
    ) -> None:
        self.verify = verify
        self.proxy = proxy
        self.inner = transport
        self.sync: httpx.BaseTransport | None = None
        self.async_: httpx.AsyncBaseTransport | None = None
        self.lock = threading.Lock()


class TalkiTransport(httpx.BaseTransport, httpx.AsyncBaseTransport):
    def __init__(
        self,
        *,
        max_retries: int = 2,
        auto_idempotency: bool = True,
        verify: ssl.SSLContext | str | bool = True,
        proxy: str | None = None,
        transport: httpx.BaseTransport | httpx.AsyncBaseTransport | None = None,
        sleep: Callable[[float], None] = time.sleep,
        async_sleep: Callable[[float], Awaitable[None]] = anyio.sleep,
        jitter: Callable[[], float] = random.random,
    ) -> None:
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        self.max_retries = max_retries
        self.auto_idempotency = auto_idempotency
        self._connections = _Connections(verify, proxy, transport)
        self._sleep = sleep
        self._async_sleep = async_sleep
        self._jitter = jitter

    def with_retries(self, max_retries: int) -> TalkiTransport:
        """A copy that retries ``max_retries`` times, on the same connections.
        Closing either closes them for both, and the next request reopens them."""
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        copy = TalkiTransport.__new__(TalkiTransport)
        copy.__dict__.update(self.__dict__)
        copy.max_retries = max_retries
        return copy

    # The request, before the first attempt.

    def _prepare(self, request: httpx.Request) -> None:
        if IDEMPOTENCY_HEADER in request.headers and not _key(request):
            # The API reads a blank key as none: send none, or a real one.
            del request.headers[IDEMPOTENCY_HEADER]
        if self.auto_idempotency and request.method in WRITE_METHODS and not _key(request):
            request.headers[IDEMPOTENCY_HEADER] = new_idempotency_key()

    @staticmethod
    def _resendable(request: httpx.Request) -> bool:
        return isinstance(request.stream, httpx.ByteStream)

    def _repeat_harmless(self, request: httpx.Request) -> bool:
        return self._resendable(request) and (request.method in SAFE_METHODS or bool(_key(request)))

    # When to try again, and after how long.

    def _backoff(self, attempt: int) -> float:
        return min(BACKOFF_CAP, BACKOFF_BASE * 2.0**attempt) * (0.5 + self._jitter() / 2)

    def _needs_body(self, request: httpx.Request, response: httpx.Response, attempt: int) -> bool:
        """Whether deciding on a retry means reading the answer's body."""
        return (
            attempt < self.max_retries
            and self._resendable(request)
            and (
                response.status_code == 409
                or (request.method not in SAFE_METHODS and response.status_code in GATEWAY_STATUSES)
            )
        )

    def _retryable(self, request: httpx.Request, response: httpx.Response, body: bytes | None) -> bool:
        status = response.status_code
        if status == 429:
            return self._resendable(request)
        if status == 409:
            return self._resendable(request) and _envelope_code(response, body) == "request_in_progress"
        if request.method in SAFE_METHODS:
            return status in SAFE_RETRY_STATUSES and self._resendable(request)
        return (
            status in GATEWAY_STATUSES
            and not request.extensions.get(UNSENT_ONLY)
            and self._repeat_harmless(request)
            and _envelope_code(response, body) is None
        )

    def _delay(
        self, request: httpx.Request, response: httpx.Response, body: bytes | None, attempt: int
    ) -> float | None:
        if attempt >= self.max_retries or not self._retryable(request, response, body):
            return None
        asked = retry_after_seconds(response.headers)
        if asked is None:
            return self._backoff(attempt)
        return asked if asked <= MAX_RETRY_AFTER else None

    def _after_error(self, request: httpx.Request, error: Exception, attempt: int) -> float | None:
        if attempt >= self.max_retries or not self._resendable(request):
            return None
        # What may have arrived is sent again only when it reads.
        if isinstance(error, NOT_SENT) or (isinstance(error, _MAYBE_SENT) and request.method in SAFE_METHODS):
            return self._backoff(attempt)
        return None

    @staticmethod
    def _buffered(response: httpx.Response, raw: bytes, request: httpx.Request) -> tuple[httpx.Response, bytes]:
        """A fresh, unread copy of an answer whose raw body was read here, so
        the client still decodes, times and closes it as its own; and the body
        decoded (gzip and the like undone), to look into."""

        def copy() -> httpx.Response:
            return httpx.Response(
                response.status_code,
                headers=response.headers,
                # A stream, not `content=`: a response built with content
                # counts as read, and the client would never time or close it.
                stream=httpx.ByteStream(raw),
                extensions=response.extensions,
                request=request,
            )

        probe = copy()
        try:
            body = probe.read()
        except httpx.DecodingError:
            body = b""
        return copy(), body

    def _proxy_config(self) -> httpx.Proxy | None:
        # An `httpx.Proxy`, which every supported httpx takes; a plain URL
        # only from 0.26.
        proxy = self._connections.proxy
        return httpx.Proxy(proxy) if proxy else None

    # Sync.

    def _sync_transport(self) -> httpx.BaseTransport:
        connections = self._connections
        with connections.lock:
            if connections.sync is None:
                if connections.inner is None:
                    connections.sync = httpx.HTTPTransport(verify=connections.verify, proxy=self._proxy_config())
                elif isinstance(connections.inner, httpx.BaseTransport):
                    connections.sync = connections.inner
                else:
                    raise TypeError("The transport given is async only; this client was used synchronously.")
            return connections.sync

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self._prepare(request)
        attempt = 0
        while True:
            started = time.monotonic()
            try:
                response = self._sync_transport().handle_request(request)
            except httpx.TransportError as error:
                delay = self._after_error(request, error, attempt)
                if delay is None:
                    _log_failure(request, error, started)
                    raise
                _log_retry(request, type(error).__name__, delay, attempt, self.max_retries)
            else:
                body = None
                if self._needs_body(request, response, attempt):
                    if response.is_stream_consumed:  # built already read (a test double)
                        body = response.content
                    else:
                        raw = b"".join(response.iter_raw())
                        response.close()
                        response, body = self._buffered(response, raw, request)
                delay = self._delay(request, response, body, attempt)
                if delay is None:
                    _log_answer(request, response, started)
                    return response
                _log_retry(request, _answer(response), delay, attempt, self.max_retries)
                response.close()
            self._sleep(delay)
            attempt += 1

    # Forgotten once closed, so that the next request opens a new pool.
    def close(self) -> None:
        connections = self._connections
        with connections.lock:
            closing, connections.sync = connections.sync, None
        if closing is not None:
            closing.close()

    # Async.

    def _async_transport(self) -> httpx.AsyncBaseTransport:
        connections = self._connections
        with connections.lock:
            if connections.async_ is None:
                if connections.inner is None:
                    connections.async_ = httpx.AsyncHTTPTransport(verify=connections.verify, proxy=self._proxy_config())
                elif isinstance(connections.inner, httpx.AsyncBaseTransport):
                    connections.async_ = connections.inner
                else:
                    raise TypeError("The transport given is sync only; this client was used asynchronously.")
            return connections.async_

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        self._prepare(request)
        attempt = 0
        while True:
            started = time.monotonic()
            try:
                response = await self._async_transport().handle_async_request(request)
            except httpx.TransportError as error:
                delay = self._after_error(request, error, attempt)
                if delay is None:
                    _log_failure(request, error, started)
                    raise
                _log_retry(request, type(error).__name__, delay, attempt, self.max_retries)
            else:
                body = None
                if self._needs_body(request, response, attempt):
                    if response.is_stream_consumed:  # built already read (a test double)
                        body = response.content
                    else:
                        raw = b"".join([chunk async for chunk in response.aiter_raw()])
                        await response.aclose()
                        response, body = self._buffered(response, raw, request)
                delay = self._delay(request, response, body, attempt)
                if delay is None:
                    _log_answer(request, response, started)
                    return response
                _log_retry(request, _answer(response), delay, attempt, self.max_retries)
                await response.aclose()
            await self._async_sleep(delay)
            attempt += 1

    async def aclose(self) -> None:
        connections = self._connections
        with connections.lock:
            closing, connections.async_ = connections.async_, None
        if closing is not None:
            await closing.aclose()


def _answer(response: httpx.Response) -> str:
    """A status and, when the API gave one, the request ID to quote to Talki."""
    request_id = response.headers.get(REQUEST_ID_HEADER)
    return f"{response.status_code}, request {request_id}" if request_id else str(response.status_code)


def _log_answer(request: httpx.Request, response: httpx.Response, started: float) -> None:
    if logger.isEnabledFor(logging.DEBUG):
        elapsed = (time.monotonic() - started) * 1000
        logger.debug("%s %s: %s in %.0f ms", request.method, request.url.path, _answer(response), elapsed)


def _log_failure(request: httpx.Request, error: Exception, started: float) -> None:
    if logger.isEnabledFor(logging.DEBUG):
        elapsed = (time.monotonic() - started) * 1000
        logger.debug("%s %s: %s after %.0f ms", request.method, request.url.path, type(error).__name__, elapsed)


def _log_retry(request: httpx.Request, outcome: str, delay: float, attempt: int, max_retries: int) -> None:
    logger.info(
        "%s %s: %s; retry %d of %d in %.1f s",
        request.method,
        request.url.path,
        outcome,
        attempt + 1,
        max_retries,
        delay,
    )
