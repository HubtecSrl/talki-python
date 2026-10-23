"""`unwrap`, which turns an answer into its value or an exception, and
`Resource`, the base of the generated resource classes (`talki.calls`, …).

It imports nothing from `talki.api`, so the generated packages there can
import it while `Talki` imports them.
"""

from __future__ import annotations

from typing import Any, TypeVar, cast

from .client import AuthenticatedClient
from .exceptions import ApiError, error_from
from .models import ErrorEnvelope
from .types import Response

__all__ = ["Resource", "unwrap"]

T = TypeVar("T")


class Resource:
    """One tag's operations, sent through ``client``."""

    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client


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
