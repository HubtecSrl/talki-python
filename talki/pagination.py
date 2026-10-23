"""Every page of a list, or every row: a cursor loop written once.

    from talki.pagination import pages, position, rows
    from talki.api.calls import list_calls
    from talki.api.appointments import list_appointments

    for call in rows(pages(list_calls.sync_detailed, client=talki.client, limit=100)):
        ...

    # A change feed: store each page's position, resume from it next time.
    for page in pages(list_appointments.sync_detailed, client=talki.client, cursor=stored):
        save(page.data)
        stored = position(page, stored)

The first argument is the `sync_detailed` of an operation that takes `cursor=` (or `asyncio_detailed`
for `apages`); every keyword goes to it, `cursor` included. A page is the
operation's own list model, so `data`, and what `rows` / `arows` yield, keep
its row type.

`next_cursor` comes back on a feed's last page too: it is a position, not a
promise of more, so the loop ends on `has_more` alone. Keep the filters the same
for a whole walk.
"""

from __future__ import annotations

from collections.abc import (
    AsyncIterable,
    AsyncIterator,
    Callable,
    Coroutine,
    Iterable,
    Iterator,
    Sequence,
)
from typing import Any, Protocol, TypeVar

from ._talki import unwrap
from .exceptions import TalkiError
from .models import ErrorEnvelope
from .types import UNSET, Response, Unset

__all__ = ["PaginationError", "apages", "arows", "pages", "position", "rows"]

R = TypeVar("R", covariant=True)


class PaginationError(TalkiError):
    """A page said `has_more` but gave no new `next_cursor` to ask for it."""


class ListPage(Protocol[R]):
    @property
    def data(self) -> Sequence[R]: ...
    @property
    def has_more(self) -> bool | Unset: ...
    @property
    def next_cursor(self) -> str | None | Unset: ...


P = TypeVar("P", bound=ListPage[Any])
T = TypeVar("T")


def position(page: ListPage[Any], previous: str | None = None) -> str | None:
    """Where a change-feed walk stands after ``page``: its `next_cursor`, or
    ``previous`` when the page carried none (a feed's page comes back empty).

    For change feeds only: a plain list's last page has a null `next_cursor`
    although it holds rows, so this would hand back the cursor before it."""
    cursor = page.next_cursor
    return cursor if isinstance(cursor, str) else previous


def _next(page: ListPage[Any], cursor: str | None) -> str | None:
    """The cursor for the page after ``page``, or None when there is none."""
    if not page.has_more:
        return None
    following = position(page, None)
    if following is None or following == cursor:
        # More promised and no way to ask for it: stop rather than loop forever.
        raise PaginationError("The page says has_more but gives no new next_cursor.")
    return following


def pages(
    operation: Callable[..., Response[P | ErrorEnvelope]],
    /,
    *,
    cursor: str | None = None,
    **params: Any,
) -> Iterator[P]:
    """Every page from ``cursor`` (the start when None) until `has_more` is false.
    Raises the `ApiError` of a page that fails, after yielding those before it."""
    while True:
        page = unwrap(operation(cursor=cursor if cursor is not None else UNSET, **params))
        yield page
        following = _next(page, cursor)
        if following is None:
            return
        cursor = following


def rows(pages: Iterable[ListPage[T]]) -> Iterator[T]:
    """Every row of every page, in order."""
    for page in pages:
        yield from page.data


async def apages(
    operation: Callable[..., Coroutine[Any, Any, Response[P | ErrorEnvelope]]],
    /,
    *,
    cursor: str | None = None,
    **params: Any,
) -> AsyncIterator[P]:
    """`pages` for an operation's `asyncio_detailed`."""
    while True:
        page = unwrap(await operation(cursor=cursor if cursor is not None else UNSET, **params))
        yield page
        following = _next(page, cursor)
        if following is None:
            return
        cursor = following


async def arows(pages: AsyncIterable[ListPage[T]]) -> AsyncIterator[T]:
    """`rows` for `apages`."""
    async for page in pages:
        for row in page.data:
            yield row
