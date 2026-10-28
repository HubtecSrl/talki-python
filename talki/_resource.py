"""`unwrap`, which turns an answer into its value or an exception;
`RawResponse`, an answer with its value; and `Resource`, the base of the
generated resource classes (`talki.calls`, …).

It imports nothing from `talki.api`, so the generated packages there can
import it while `Talki` imports them.
"""

from __future__ import annotations

import datetime
import enum
import uuid
from collections.abc import Callable, Mapping, MutableMapping
from typing import Any, Generic, TypeVar, cast

from .client import AuthenticatedClient
from .exceptions import REQUEST_ID_HEADER, ApiError, error_from
from .models import ErrorEnvelope
from .types import Response, Unset

__all__ = ["RawResponse", "Resource", "as_body", "raw", "unwrap"]

T = TypeVar("T")
U = TypeVar("U")
M = TypeVar("M")


class Resource:
    """One tag's operations, sent through ``client``."""

    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client


class RawResponse(Generic[T]):
    """A successful answer, as `talki.<tag>.with_raw_response.<method>()`
    returns it: its `status_code`, `headers` and `content`, and `parse()`, the
    value the method itself returns.

        raw = talki.account.with_raw_response.get()
        account, etag = raw.parse(), raw.headers["ETag"]
    """

    def __init__(self, response: Response[Any], value: T) -> None:
        self._response = response
        self.status_code = int(response.status_code)
        # Case-insensitive: `headers["etag"]` finds `ETag`.
        self.headers: MutableMapping[str, str] = response.headers
        self.content = response.content
        self._value = value

    @property
    def request_id(self) -> str | None:
        """The `X-Request-Id` to quote to Talki about this request."""
        return self.headers.get(REQUEST_ID_HEADER)

    def parse(self) -> T:
        """The value the method returns: the model, a page, or None for
        `204 No Content`."""
        return self._value

    def map(self, function: Callable[[T], U]) -> RawResponse[U]:
        """The same answer with ``function`` of its value."""
        return RawResponse(self._response, function(self._value))

    def __repr__(self) -> str:
        return f"RawResponse(status_code={self.status_code}, request_id={self.request_id!r})"


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


def raw(response: Response[T | ErrorEnvelope]) -> RawResponse[T]:
    """A `*_detailed` answer as a `RawResponse`, or the exception `unwrap` raises."""
    return RawResponse(response, unwrap(response))


class _JsonBody:
    """A dict passed as `body=`, sent as written: the generated operations only
    ever call a body's `to_dict()`."""

    def __init__(self, body: Mapping[str, Any]) -> None:
        self._json = _json(body)

    def to_dict(self) -> Any:
        return self._json


def as_body(body: M | Mapping[str, Any], model: type[M]) -> M:
    """``body`` as the operation takes it: a ``model`` as it is, a dict (a
    `<Model>Dict`) wrapped to be sent as written. The API checks it, as it does
    a model: an unknown key or a wrong type is refused with `400`."""
    if isinstance(body, Mapping):
        # Stands in for the model, whose `to_dict()` is all an operation calls.
        return cast(M, _JsonBody(body))
    return body


def _json(value: Any) -> Any:
    """``value`` in the JSON form the API reads: a nested model by its
    `to_dict()`, an enum by its value, a date, datetime or time as ISO 8601, a
    UUID as text, a set as a list. `UNSET`, as a value or an item, is left out."""
    if isinstance(value, Mapping):
        return {str(key): _json(item) for key, item in value.items() if not isinstance(item, Unset)}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json(item) for item in value if not isinstance(item, Unset)]
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, (datetime.date, datetime.time)):  # a datetime is a date
        return value.isoformat()
    if isinstance(value, uuid.UUID):
        return str(value)
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return to_dict()
    return value
