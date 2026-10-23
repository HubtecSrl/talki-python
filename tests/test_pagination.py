"""`talki.pagination`: walking lists and change feeds
through generated operations, against an `httpx.MockTransport`."""

import asyncio

import httpx
import pytest

from talki import InvalidRequestError, Talki
from talki.api.calls import list_calls
from talki.api.contacts import list_contacts
from talki.models import Contact
from talki.pagination import PaginationError, apages, arows, pages, position, rows
from talki.types import Response


def contact(n: int) -> dict:
    return {
        "id": f"00000000-0000-0000-0000-{n:012d}",
        "phone_number": f"+3934800000{n:02d}",
        "first_name": None,
        "last_name": None,
        "display_name": None,
        "notes": None,
        "last_call_at": None,
        "call_count": 0,
        "created_at": "2026-10-01T08:00:00+00:00",
        "updated_at": "2026-10-01T08:00:00+00:00",
    }


def answer(numbers: list[int], *, has_more: bool | None, next_cursor: str | None) -> httpx.Response:
    body: dict = {"object": "list", "data": [contact(n) for n in numbers], "next_cursor": next_cursor}
    if has_more is not None:
        body["has_more"] = has_more
    return httpx.Response(200, json=body)


class Feed:
    """Answers by the `cursor` each request carries, and keeps the queries."""

    def __init__(self, by_cursor: dict[str | None, httpx.Response]) -> None:
        self.by_cursor = by_cursor
        self.queries: list[httpx.QueryParams] = []

    @property
    def cursors(self) -> list[str | None]:
        return [query.get("cursor") for query in self.queries]

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.queries.append(request.url.params)
        return self.by_cursor[request.url.params.get("cursor")]


def talki_for(feed: Feed) -> Talki:
    return Talki(api_key="talki_test_x", transport=httpx.MockTransport(feed), max_retries=0)


def three_pages() -> Feed:
    return Feed(
        {
            None: answer([1, 2], has_more=True, next_cursor="c1"),
            "c1": answer([3], has_more=True, next_cursor="c2"),
            "c2": answer([4], has_more=False, next_cursor="c3"),
        }
    )


def test_every_row_of_every_page_in_order():
    feed = three_pages()
    with talki_for(feed) as talki:
        walked = list(rows(pages(list_contacts.sync_detailed, client=talki.client, limit=2)))
    assert all(isinstance(row, Contact) for row in walked)
    assert [row.phone_number[-2:] for row in walked] == ["01", "02", "03", "04"]
    assert feed.cursors == [None, "c1", "c2"]
    assert all(query["limit"] == "2" for query in feed.queries)


def test_a_walk_resumes_from_a_stored_cursor_and_reports_where_it_stands():
    feed = three_pages()
    stored: str | None = "c1"
    with talki_for(feed) as talki:
        for page in pages(list_contacts.sync_detailed, client=talki.client, cursor=stored):
            stored = position(page, stored)
    assert feed.cursors == ["c1", "c2"]
    # The last page's cursor is the position, though nothing follows it.
    assert stored == "c3"


def test_an_empty_page_keeps_the_position_it_had():
    feed = Feed({"c9": answer([], has_more=False, next_cursor=None)})
    stored: str | None = "c9"
    with talki_for(feed) as talki:
        for page in pages(list_contacts.sync_detailed, client=talki.client, cursor=stored):
            stored = position(page, stored)
    assert stored == "c9"


def test_a_failing_page_raises_after_the_pages_before_it():
    refused = httpx.Response(
        400, json={"error": {"type": "invalid_request", "code": "invalid_cursor", "message": "m", "request_id": "r"}}
    )
    feed = Feed({None: answer([1], has_more=True, next_cursor="c1"), "c1": refused})
    seen = []
    with talki_for(feed) as talki:
        with pytest.raises(InvalidRequestError) as raised:
            for page in pages(list_contacts.sync_detailed, client=talki.client):
                seen.append(page)
    assert len(seen) == 1
    assert raised.value.code == "invalid_cursor"


@pytest.mark.parametrize("repeated", [None, "c0"], ids=["no-cursor", "same-cursor"])
def test_more_promised_without_a_new_cursor_stops_instead_of_looping(repeated):
    feed = Feed({"c0": answer([1], has_more=True, next_cursor=repeated)})
    with talki_for(feed) as talki:
        with pytest.raises(PaginationError):
            list(pages(list_contacts.sync_detailed, client=talki.client, cursor="c0"))
    assert feed.cursors == ["c0"]


def test_every_page_carries_the_same_filters():
    calls = {"object": "list", "has_more": True, "next_cursor": "c1", "data": []}
    last = {**calls, "has_more": False, "next_cursor": "c2"}
    feed = Feed({None: httpx.Response(200, json=calls), "c1": httpx.Response(200, json=last)})
    location = "11111111-1111-1111-1111-111111111111"
    with talki_for(feed) as talki:
        list(pages(list_calls.sync_detailed, client=talki.client, sync=True, location_id=location, limit=10))
    assert feed.cursors == [None, "c1"]
    for query in feed.queries:
        assert (query["sync"], query["location_id"], query["limit"]) == ("true", location, "10")


def test_the_async_walk_raises_a_failing_page_too():
    refused = httpx.Response(
        400, json={"error": {"type": "invalid_request", "code": "invalid_cursor", "message": "m", "request_id": "r"}}
    )
    feed = Feed({None: answer([1], has_more=True, next_cursor="c1"), "c1": refused})

    async def walk() -> list[Contact]:
        seen = []
        async with talki_for(feed) as talki:
            async for row in arows(apages(list_contacts.asyncio_detailed, client=talki.client)):
                seen.append(row)
        return seen

    with pytest.raises(InvalidRequestError):
        asyncio.run(walk())


def test_response_stays_covariant():
    # pages/rows infer row types only while the generated Response is covariant
    # in its parsed type (codegen/templates/types.py.jinja).
    (parameter,) = Response.__parameters__
    assert parameter.__covariant__


def test_the_async_walk_matches_the_sync_one():
    feed = three_pages()

    async def walk() -> list[Contact]:
        async with talki_for(feed) as talki:
            return [row async for row in arows(apages(list_contacts.asyncio_detailed, client=talki.client))]

    walked = asyncio.run(walk())
    assert [row.phone_number[-2:] for row in walked] == ["01", "02", "03", "04"]
    assert feed.cursors == [None, "c1", "c2"]
