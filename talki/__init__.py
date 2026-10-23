"""A client library for accessing Talki API"""

# The contract this package was generated from, sent as `Talki-Version` by
# `Talki` unless told otherwise.
API_VERSION = "2026-10-01"

from ._talki import Talki, unwrap
from ._transport import new_idempotency_key
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
    "AuthenticatedClient",
    "AuthenticationError",
    "Client",
    "ConflictError",
    "InvalidRequestError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "Talki",
    "TalkiError",
    "new_idempotency_key",
    "unwrap",
)
