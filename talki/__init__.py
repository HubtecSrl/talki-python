"""A client library for accessing Talki API"""

# The contract this package was generated from, sent as `Talki-Version` by
# `Talki` unless told otherwise.
API_VERSION = "2026-10-01"

from ._resource import RawResponse
from ._talki import AsyncTalki, Talki, unwrap
from ._transport import new_idempotency_key
from ._version import __version__
from .client import AuthenticatedClient, Client
from .exceptions import (
    ApiError,
    AuthenticationError,
    ConflictError,
    InvalidRequestError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    TalkiError,
)

__all__ = (
    "API_VERSION",
    "ApiError",
    "AsyncTalki",
    "AuthenticatedClient",
    "AuthenticationError",
    "Client",
    "ConflictError",
    "InvalidRequestError",
    "PermissionDeniedError",
    "RateLimitError",
    "RawResponse",
    "ServerError",
    "Talki",
    "TalkiError",
    "__version__",
    "new_idempotency_key",
    "unwrap",
)
