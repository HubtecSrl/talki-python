"""Every page of a list, or every row: a cursor loop written once.

A list that takes `cursor` returns a `Page` (`AsyncPage` on `AsyncTalki`): the
first page, fetched by the call, whose iteration fetches the rest.

    for call in talki.calls.list(limit=100):     # every row, page after page
        ...

    # A change feed: store each page's position, resume from it next time.
    for page in talki.appointments.list(cursor=stored).iter_pages():
        save(page.data)
        stored = position(page, stored)

    async for call in await talki.calls.list():  # AsyncTalki
        ...

`pages` and `rows` (`apages` and `arows`) do the same for an operation under
`talki.api`, when its `Response` is wanted:

    for call in rows(pages(list_calls.sync_detailed, client=talki.client, limit=100)):
        ...

Their first argument is the `sync_detailed` of an operation that takes `cursor=`
(or `asyncio_detailed` for `apages`); every keyword goes to it, `cursor`
included. A page is then the operation's own list model, so `data`, and what
`rows` / `arows` yield, keep its row type.

`next_cursor` comes back on a feed's last page too: it is a position, not a
promise of more, so the loop ends on `has_more` alone. Keep the filters the same
for a whole walk.
"""

from __future__ import annotations

from collections.abc import (
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Coroutine,
    Iterable,
    Iterator,
    Sequence,
)
from typing import Any, Generic, Protocol, TypeVar

from ._resource import unwrap
from .exceptions import TalkiError
from .models import ErrorEnvelope
from .types import UNSET, Response, Unset

__all__ = ["AsyncPage", "Page", "PaginationError", "apages", "arows", "pages", "position", "rows"]

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


class Page(Generic[T]):
    """One page of a list, as a resource method returns it: its rows in `data`,
    `has_more` and `next_cursor`.

    Iterating a page yields its rows and those of every page after it,
    fetched as the loop reaches them; `iter_pages` yields the pages. Either
    starts again from this page each time. Raises the `ApiError` of a page that
    fails, after yielding those before it.
    """

    def __init__(
        self,
        page: ListPage[T],
        fetch: Callable[[str | None | Unset], ListPage[T]],
        cursor: str | None | Unset,
    ) -> None:
        self.data: list[T] = list(page.data)
        self.has_more = bool(page.has_more)
        self.next_cursor = position(page)
        self._fetch = fetch
        self._cursor = cursor if isinstance(cursor, str) else None

    @classmethod
    def first(cls, fetch: Callable[[str | None | Unset], ListPage[T]], cursor: str | None | Unset) -> Page[T]:
        """The page at ``cursor``, fetched with ``fetch``, which later pages use too."""
        return cls(fetch(cursor), fetch, cursor)

    def iter_pages(self) -> Iterator[Page[T]]:
        """This page, then every page after it."""
        page = self
        while True:
            yield page
            following = _next(page, page._cursor)
            if following is None:
                return
            page = Page.first(self._fetch, following)

    def __iter__(self) -> Iterator[T]:
        for page in self.iter_pages():
            yield from page.data

    def __repr__(self) -> str:
        return f"Page(rows={len(self.data)}, has_more={self.has_more}, next_cursor={self.next_cursor!r})"


class AsyncPage(Generic[T]):
    """`Page` for `AsyncTalki`: ``async for`` it, and `iter_pages` yields with
    ``async for`` too."""

    def __init__(
        self,
        page: ListPage[T],
        fetch: Callable[[str | None | Unset], Awaitable[ListPage[T]]],
        cursor: str | None | Unset,
    ) -> None:
        self.data: list[T] = list(page.data)
        self.has_more = bool(page.has_more)
        self.next_cursor = position(page)
        self._fetch = fetch
        self._cursor = cursor if isinstance(cursor, str) else None

    @classmethod
    async def first(
        cls, fetch: Callable[[str | None | Unset], Awaitable[ListPage[T]]], cursor: str | None | Unset
    ) -> AsyncPage[T]:
        """The page at ``cursor``, fetched with ``fetch``, which later pages use too."""
        return cls(await fetch(cursor), fetch, cursor)

    async def iter_pages(self) -> AsyncIterator[AsyncPage[T]]:
        """This page, then every page after it."""
        page = self
        while True:
            yield page
            following = _next(page, page._cursor)
            if following is None:
                return
            page = await AsyncPage.first(self._fetch, following)

    async def __aiter__(self) -> AsyncIterator[T]:
        async for page in self.iter_pages():
            for row in page.data:
                yield row

    def __repr__(self) -> str:
        return f"AsyncPage(rows={len(self.data)}, has_more={self.has_more}, next_cursor={self.next_cursor!r})"
