"""What `Talki` and `unwrap` raise: one class per error `type` of the API's
envelope, so a caller can catch the kind of failure it handles.

Branch on `code` within a class; `message` is for people. An answer with no
envelope (a proxy's 502, an undeclared status) raises the class its HTTP status
implies, with `code` and `type` None.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import UTC
from email.utils import parsedate_to_datetime
from time import time
from typing import Any

import httpx

__all__ = [
    "ApiError",
    "AuthenticationError",
    "ConflictError",
    "InvalidRequestError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "TalkiError",
]

REQUEST_ID_HEADER = "X-Request-Id"


class TalkiError(Exception):
    """Every exception this package raises on purpose."""


class ApiError(TalkiError):
    """The API refused the request, or answered in a way this client cannot read."""

    def __init__(
        self,
        *,
        status: int,
        code: str | None = None,
        type: str | None = None,
        message: str = "",
        request_id: str | None = None,
        headers: Mapping[str, str] | None = None,
        body: bytes = b"",
    ) -> None:
        self.status = status
        self.code = code
        self.type = type
        self.message = message
        self.request_id = request_id
        self.headers: Mapping[str, str] = headers or {}
        self.body = body
        super().__init__(str(self))

    def __str__(self) -> str:
        text = f"HTTP {self.status} {self.code or 'unexpected_response'}"
        if self.message:
            text += f": {self.message}"
        if self.request_id:
            text += f" (request {self.request_id})"
        return text

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self})"

    def __reduce__(self) -> tuple[Any, ...]:
        # Rebuilt from its fields, so it survives pickle and copy (a worker
        # process, a task queue).
        return (_restore, (type(self), self._fields()))

    def _fields(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "code": self.code,
            "type": self.type,
            "message": self.message,
            "request_id": self.request_id,
            # httpx's raw byte pairs: never re-encoded, repeated headers kept.
            "headers": list(self.headers.raw) if isinstance(self.headers, httpx.Headers) else dict(self.headers),
            "body": self.body,
        }


def _restore(cls: type[ApiError], fields: dict[str, Any]) -> ApiError:
    headers = fields["headers"]
    return cls(**{**fields, "headers": httpx.Headers(headers) if isinstance(headers, list) else headers})


class InvalidRequestError(ApiError):
    """`invalid_request`: fix the request; retrying it unchanged fails again."""


class AuthenticationError(ApiError):
    """`authentication_error`: the credential is missing, wrong, expired or revoked."""


class PermissionDeniedError(ApiError):
    """`permission_error`: the credential is valid but may not do this."""


class ConflictError(ApiError):
    """`conflict`: the request clashes with the resource's current state."""


class RateLimitError(ApiError):
    """`rate_limit_error`: too many requests. `retry_after` is the wait the API
    asked for, in seconds, when it said."""

    @property
    def retry_after(self) -> float | None:
        return retry_after_seconds(self.headers)


class ServerError(ApiError):
    """`api_error`, or a 5xx with no envelope: the failure is on Talki's side."""


_BY_TYPE: dict[str, type[ApiError]] = {
    "invalid_request": InvalidRequestError,
    "authentication_error": AuthenticationError,
    "permission_error": PermissionDeniedError,
    "conflict": ConflictError,
    "rate_limit_error": RateLimitError,
    "api_error": ServerError,
}

_BY_STATUS: dict[int, type[ApiError]] = {
    400: InvalidRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    409: ConflictError,
    429: RateLimitError,
}


def _class_for(type_: str | None, status: int) -> type[ApiError]:
    if type_ in _BY_TYPE:
        return _BY_TYPE[type_]
    if type_ is None:
        if status >= 500:
            return ServerError
        return _BY_STATUS.get(status, ApiError)
    # A type this client predates: the base class, which every caller catches.
    return ApiError


def error_from(status: int, headers: Mapping[str, str], body: bytes) -> ApiError:
    """The exception for one answer, read from its envelope when it has one."""
    try:
        payload = json.loads(body) if body else None
    except ValueError:
        payload = None
    detail = payload.get("error") if isinstance(payload, dict) else None
    if isinstance(detail, dict):
        type_ = detail.get("type") if isinstance(detail.get("type"), str) else None
        return _class_for(type_, status)(
            status=status,
            code=_text(detail.get("code")),
            type=type_,
            message=str(detail.get("message") or ""),
            request_id=_text(detail.get("request_id")) or headers.get(REQUEST_ID_HEADER),
            headers=headers,
            body=body,
        )
    return _class_for(None, status)(
        status=status,
        message=body[:300].decode("utf-8", "replace") if body else "",
        request_id=headers.get(REQUEST_ID_HEADER),
        headers=headers,
        body=body,
    )


def _text(value: object) -> str | None:
    return value if isinstance(value, str) else None


def retry_after_seconds(headers: Mapping[str, str]) -> float | None:
    """`Retry-After` as seconds from now (it may be a number or an HTTP date)."""
    raw = next((value for key, value in headers.items() if str(key).lower() == "retry-after"), None)
    if not raw:
        return None
    try:
        return max(0.0, float(raw))
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        # A date ending `-0000` parses without a zone; HTTP dates are UTC.
        when = when.replace(tzinfo=UTC)
    return max(0.0, when.timestamp() - time())
