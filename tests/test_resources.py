"""The resource methods (`talki.calls.list()`, …) generated per tag, and the
`Page` a list returns, against an `httpx.MockTransport`."""

import asyncio
import datetime
import inspect
import json
import typing
import uuid

import attrs
import httpx
import pytest

import talki.api
from talki import AsyncTalki, ConflictError, InvalidRequestError, RawResponse, Talki
from talki.api import AsyncResources, Resources
from talki.models import CallCount, CallerRuleKind, Contact, Tag, TagCreate, WorkingHours, WorkingHoursSlot
from talki.pagination import AsyncPage, AsyncPager, Page, PaginationError, position
from talki.types import UNSET, File

# The public surface. A method renamed or dropped by a regeneration (a new
# operation can take a name another one had) fails here instead of in a
# caller's code: change it with a changelog line, as a breaking change.
METHODS = {
    "account": ["complete_onboarding", "get", "get_forwarding_check", "start_forwarding_check", "update"],
    "appointments": ["cancel", "create", "get", "list", "reschedule", "restore"],
    "availability": ["get"],
    "caller_rules": ["create", "delete", "list", "list_blocked_call_attempts", "update"],
    "calls": [
        "count",
        "count_refused",
        "delete",
        "export_call",
        "export_calls",
        "get",
        "get_refused_summary",
        "get_stats",
        "get_transcript",
        "list",
        "list_refused",
        "mark_all_read",
        "update",
    ],
    "closures": ["create", "delete", "list", "update"],
    "contacts": ["delete", "get", "list", "upsert"],
    "locations": ["list"],
    "pending_contacts": ["approve", "discard", "list"],
    "resources": ["create", "delete", "get", "list", "update"],
    "sandbox": ["create_call", "list_scenarios", "reset"],
    "services": ["create", "delete", "get", "list", "update"],
    "tags": ["create", "delete", "list", "tag_contact", "untag_contact", "update"],
    "unresolved_requests": ["get", "list", "teach", "update"],
    "usage": ["get", "get_history"],
    "voices": ["get_preview", "list"],
    "working_hours": ["get", "replace"],
}

TAG = {
    "id": "00000000-0000-0000-0000-0000000000aa",
    "name": "VIP",
    "color": "#ff0000",
    "contact_ids": [],
    "created_at": "2026-10-01T08:00:00+00:00",
}


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


def contacts(numbers: list[int], *, has_more: bool, next_cursor: str | None) -> httpx.Response:
    body = {"object": "list", "data": [contact(n) for n in numbers], "has_more": has_more, "next_cursor": next_cursor}
    return httpx.Response(200, json=body)


class Server:
    """Answers by path and `cursor`, and keeps every request."""

    def __init__(self, answers: dict[tuple[str, str | None], httpx.Response]) -> None:
        self.answers = answers
        self.requests: list[httpx.Request] = []

    @property
    def cursors(self) -> list[str | None]:
        return [request.url.params.get("cursor") for request in self.requests]

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return self.answers[(request.url.path, request.url.params.get("cursor"))]


def sync_for(server: Server) -> Talki:
    return Talki(api_key="talki_test_x", transport=httpx.MockTransport(server), max_retries=0)


def async_for(server: Server) -> AsyncTalki:
    return AsyncTalki(api_key="talki_test_x", transport=httpx.MockTransport(server), max_retries=0)


def three_pages() -> Server:
    return Server(
        {
            ("/v1/contacts", None): contacts([1, 2], has_more=True, next_cursor="c1"),
            ("/v1/contacts", "c1"): contacts([3], has_more=True, next_cursor="c2"),
            ("/v1/contacts", "c2"): contacts([4], has_more=False, next_cursor="c3"),
        }
    )


def public(resource: type) -> list[str]:
    """The methods of ``resource``, without `with_raw_response`."""
    return sorted(name for name in vars(resource) if not name.startswith("_") and name != "with_raw_response")


def raw_class(resource: type) -> type:
    return inspect.signature(vars(resource)["with_raw_response"].func).return_annotation


def resource_classes(mixin: type) -> dict[str, type]:
    return {
        name: _resolved(inspect.signature(value.func).return_annotation, value.func)
        for name, value in vars(mixin).items()
        if not name.startswith("_") and hasattr(value, "func")
    }


def _resolved(annotation: object, function: typing.Any) -> typing.Any:
    """An annotation, evaluated when a module's postponed annotations left it a string."""
    return eval(annotation, function.__globals__) if isinstance(annotation, str) else annotation


# The surface


def test_every_tag_is_a_resource_with_the_methods_it_had():
    assert {tag: public(resource) for tag, resource in resource_classes(Resources).items()} == METHODS


def test_the_async_resources_mirror_the_sync_ones_signature_for_signature():
    sync, async_ = resource_classes(Resources), resource_classes(AsyncResources)
    assert sync.keys() == async_.keys()
    for tag, resource in sync.items():
        assert public(async_[tag]) == public(resource)
        for name in public(resource):
            method, awaited = getattr(resource, name), getattr(async_[tag], name)
            assert not inspect.iscoroutinefunction(method)
            # A list that pages returns an `AsyncPager`, awaited or iterated;
            # every other method is a coroutine.
            pages = "cursor" in inspect.signature(method).parameters
            assert inspect.iscoroutinefunction(awaited) != pages, f"{tag}.{name}"
            sync_parameters = inspect.signature(method).parameters
            async_parameters = inspect.signature(awaited).parameters
            assert list(sync_parameters) == list(async_parameters), f"{tag}.{name}"


def test_every_resource_has_its_methods_with_the_raw_response_too():
    for mixin in (Resources, AsyncResources):
        for tag, resource in resource_classes(mixin).items():
            raw = raw_class(resource)
            assert public(raw) == public(resource), tag
            for name in public(resource):
                assert list(inspect.signature(getattr(raw, name)).parameters) == list(
                    inspect.signature(getattr(resource, name)).parameters
                ), f"{tag}.{name}"
                assert inspect.iscoroutinefunction(getattr(raw, name)) == (mixin is AsyncResources)


def test_no_tag_is_shadowed_by_an_attribute_of_the_client():
    client = Talki(api_key="talki_test_x")
    for tag in METHODS:
        assert tag not in vars(client)
        assert isinstance(getattr(client, tag), talki._resource.Resource)
    # Built once per client.
    assert client.calls is client.calls


def test_every_operation_is_reachable_from_a_resource():
    modules = {
        name
        for tag in METHODS
        for name, value in vars(getattr(talki.api, tag)).items()
        if inspect.ismodule(value) and hasattr(value, "sync_detailed")
    }
    sources = "".join(inspect.getsource(raw_class(resource)) for resource in resource_classes(Resources).values())
    assert modules
    assert {module for module in modules if f"{module}.sync_detailed(" not in sources} == set()


def test_a_method_returns_a_page_exactly_when_it_takes_a_cursor():
    for mixin, page_type in ((Resources, Page), (AsyncResources, AsyncPager)):
        for tag, resource in resource_classes(mixin).items():
            for name in public(resource):
                signature = inspect.signature(getattr(resource, name))
                returns_page = typing.get_origin(signature.return_annotation) is page_type
                assert returns_page == ("cursor" in signature.parameters), f"{tag}.{name}"


# Sync methods


def test_a_method_returns_the_model_and_sends_its_arguments():
    server = Server({("/v1/calls/count", None): httpx.Response(200, json={"total": 7})})
    with sync_for(server) as client:
        count = client.calls.count(location_id="11111111-1111-1111-1111-111111111111")
    assert count == CallCount(total=7)
    (request,) = server.requests
    assert request.url.params["location_id"] == "11111111-1111-1111-1111-111111111111"
    assert request.headers["Talki-Version"] == talki.API_VERSION


def test_a_write_takes_a_body_and_gets_an_idempotency_key():
    server = Server({("/v1/tags", None): httpx.Response(201, json=TAG)})
    with sync_for(server) as client:
        tag = client.tags.create(body=TagCreate(name="VIP", color="#ff0000"))
    assert isinstance(tag, Tag) and tag.name == "VIP"
    (request,) = server.requests
    assert request.method == "POST"
    assert request.headers["Idempotency-Key"]
    assert json.loads(request.read()) == {"name": "VIP", "color": "#ff0000"}


def test_per_request_options_go_out_as_headers():
    server = Server({(f"/v1/tags/{TAG['id']}", None): httpx.Response(204)})
    with sync_for(server) as client:
        assert client.tags.delete(TAG["id"], idempotency_key="mine", talki_version="2026-01-01") is None
    (request,) = server.requests
    assert request.method == "DELETE"
    assert (request.headers["Idempotency-Key"], request.headers["Talki-Version"]) == ("mine", "2026-01-01")


def test_an_error_raises_its_class():
    conflict = httpx.Response(
        409, json={"error": {"type": "conflict", "code": "tag_exists", "message": "m", "request_id": "req_1"}}
    )
    server = Server({("/v1/tags", None): conflict})
    with sync_for(server) as client:
        with pytest.raises(ConflictError) as raised:
            client.tags.create(body=TagCreate(name="VIP", color="#ff0000"))
    assert raised.value.code == "tag_exists"


def test_a_binary_answer_is_a_file():
    pdf = httpx.Response(200, content=b"%PDF-1.7", headers={"content-type": "application/pdf"})
    server = Server({("/v1/calls/00000000-0000-0000-0000-000000000001/export", None): pdf})
    with sync_for(server) as client:
        exported = client.calls.export_call("00000000-0000-0000-0000-000000000001")
    assert isinstance(exported, File)
    assert exported.payload.read() == b"%PDF-1.7"


# Pages


def test_a_list_is_its_first_page():
    server = three_pages()
    with sync_for(server) as client:
        page = client.contacts.list(limit=2)
    assert isinstance(page, Page)
    assert [row.phone_number[-2:] for row in page.data] == ["01", "02"]
    assert (page.has_more, page.next_cursor) == (True, "c1")
    assert repr(page) == "Page(rows=2, has_more=True, next_cursor='c1')"
    # Only the first page is fetched until the page is iterated.
    assert server.cursors == [None]


def test_iterating_a_page_yields_every_row_from_there_on():
    server = three_pages()
    with sync_for(server) as client:
        walked = list(client.contacts.list(limit=2))
    assert all(isinstance(row, Contact) for row in walked)
    assert [row.phone_number[-2:] for row in walked] == ["01", "02", "03", "04"]
    assert server.cursors == [None, "c1", "c2"]
    assert all(request.url.params["limit"] == "2" for request in server.requests)


def test_a_feed_resumes_from_a_stored_cursor_page_by_page():
    server = three_pages()
    stored: str | None = "c1"
    with sync_for(server) as client:
        for page in client.contacts.list(cursor=stored).iter_pages():
            stored = position(page, stored)
    assert server.cursors == ["c1", "c2"]
    assert stored == "c3"


def test_iterating_again_starts_from_the_same_page():
    server = three_pages()
    with sync_for(server) as client:
        page = client.contacts.list()
        first, second = list(page), list(page)
    assert first == second
    # The first page is kept; the later ones are fetched each time.
    assert server.cursors == [None, "c1", "c2", "c1", "c2"]


def test_a_failing_first_page_raises_at_the_call():
    refused = httpx.Response(
        400, json={"error": {"type": "invalid_request", "code": "invalid_cursor", "message": "m", "request_id": "r"}}
    )
    server = Server({("/v1/contacts", "bad"): refused})
    with sync_for(server) as client:
        with pytest.raises(InvalidRequestError):
            client.contacts.list(cursor="bad")


def test_more_promised_without_a_new_cursor_stops_instead_of_looping():
    server = Server({("/v1/contacts", "c0"): contacts([1], has_more=True, next_cursor="c0")})
    with sync_for(server) as client:
        with pytest.raises(PaginationError):
            list(client.contacts.list(cursor="c0"))
    assert server.cursors == ["c0"]


def test_a_list_without_cursor_returns_its_model():
    server = Server(
        {("/v1/tags", None): httpx.Response(200, json={"data": [TAG], "has_more": False, "next_cursor": None})}
    )
    with sync_for(server) as client:
        tags = client.tags.list()
    assert not isinstance(tags, Page)
    assert [tag.name for tag in tags.data] == ["VIP"]


# Async


def test_the_async_client_awaits_the_same_methods():
    server = Server({("/v1/tags", None): httpx.Response(201, json=TAG)})

    async def run() -> Tag:
        async with async_for(server) as client:
            return await client.tags.create(body=TagCreate(name="VIP", color="#ff0000"))

    assert asyncio.run(run()).name == "VIP"
    assert server.requests[0].headers["Idempotency-Key"]


def test_an_async_page_walks_rows_and_pages():
    server = three_pages()

    async def run() -> tuple[list[str], list[int]]:
        async with async_for(server) as client:
            page = await client.contacts.list(limit=2)
            assert isinstance(page, AsyncPage)
            rows = [row.phone_number[-2:] async for row in page]
            sizes = [len(each.data) async for each in page.iter_pages()]
            return rows, sizes

    rows, sizes = asyncio.run(run())
    assert rows == ["01", "02", "03", "04"]
    assert sizes == [2, 1, 1]
    assert server.cursors == [None, "c1", "c2", "c1", "c2"]


def test_the_async_repr_never_shows_the_credential():
    assert "talki_test_x" not in repr(AsyncTalki(api_key="talki_test_x"))
    assert repr(AsyncTalki(api_key="talki_test_x")).startswith("AsyncTalki(")


# Without `with`, and closing


def test_a_client_kept_without_with_works_and_close_lets_it_go_on():
    server = Server({("/v1/calls/count", None): httpx.Response(200, json={"total": 7})})
    client = sync_for(server)
    client.close()  # nothing opened yet: a no-op
    assert client.calls.count().total == 7
    opened = client.client.get_httpx_client()
    client.close()
    assert opened.is_closed
    assert (client.client._client, client.transport._connections.sync) == (None, None)
    # Still usable: the next request opens new connections.
    assert client.calls.count().total == 7
    assert client.client.get_httpx_client() is not opened


def test_the_same_client_opens_with_with_twice():
    server = Server({("/v1/calls/count", None): httpx.Response(200, json={"total": 7})})
    client = sync_for(server)
    client.calls.count()
    for _ in range(2):
        with client as opened:
            assert opened is client
            assert client.calls.count().total == 7
        assert client.client._client is None
    assert len(server.requests) == 3


def test_the_async_client_closes_and_goes_on_too():
    server = Server({("/v1/calls/count", None): httpx.Response(200, json={"total": 7})})

    async def run() -> list[int]:
        client = async_for(server)
        totals = [(await client.calls.count()).total]
        opened = client.client.get_async_httpx_client()
        await client.aclose()
        assert opened.is_closed and client.client._async_client is None
        totals.append((await client.calls.count()).total)
        async with client:
            totals.append((await client.calls.count()).total)
        async with client:
            totals.append((await client.calls.count()).total)
        return totals

    assert asyncio.run(run()) == [7, 7, 7, 7]


# The whole answer

HOURS = {
    "location_id": "11111111-1111-1111-1111-111111111111",
    "slots": [{"days": [1], "start": "09:00", "end": "13:00"}],
}


def test_the_raw_response_has_the_headers_and_parses_to_the_value():
    server = Server(
        {
            ("/v1/working_hours", None): httpx.Response(
                200, json=HOURS, headers={"ETag": '"v1"', "X-Request-Id": "req_1"}
            )
        }
    )
    with sync_for(server) as client:
        raw = client.working_hours.with_raw_response.get()
        hours = raw.parse()
        client.working_hours.replace(body={"slots": []}, if_match=raw.headers["etag"])
    assert isinstance(raw, RawResponse)
    assert (raw.status_code, raw.request_id) == (200, "req_1")
    assert isinstance(hours, WorkingHours) and hours.slots[0].start == "09:00"
    assert json.loads(raw.content) == HOURS
    assert repr(raw) == "RawResponse(status_code=200, request_id='req_1')"
    # The `ETag` read goes back as `If-Match`.
    assert server.requests[1].headers["If-Match"] == '"v1"'
    # Built once per resource.
    assert client.working_hours.with_raw_response is client.working_hours.with_raw_response


def test_the_raw_response_of_an_error_raises_as_the_method_does():
    conflict = httpx.Response(
        409, json={"error": {"type": "conflict", "code": "tag_exists", "message": "m", "request_id": "req_1"}}
    )
    with sync_for(Server({("/v1/tags", None): conflict})) as client:
        with pytest.raises(ConflictError):
            client.tags.with_raw_response.create(body={"name": "VIP", "color": "#ff0000"})


def test_the_raw_response_of_a_list_parses_to_a_page_that_walks_on():
    server = three_pages()
    with sync_for(server) as client:
        raw = client.contacts.with_raw_response.list(limit=2)
        page = raw.parse()
        assert isinstance(page, Page) and len(page.data) == 2
        assert len(list(page)) == 4
    assert server.cursors == [None, "c1", "c2"]


def test_a_no_content_raw_response_parses_to_none():
    server = Server({(f"/v1/tags/{TAG['id']}", None): httpx.Response(204)})
    with sync_for(server) as client:
        raw = client.tags.with_raw_response.delete(TAG["id"])
    assert (raw.status_code, raw.parse()) == (204, None)


def test_the_async_raw_response_is_awaited():
    server = three_pages()

    async def run() -> tuple[int, list[str]]:
        async with async_for(server) as client:
            raw = await client.contacts.with_raw_response.list(limit=2)
            page = raw.parse()
            assert isinstance(page, AsyncPage)
            return raw.status_code, [row.phone_number[-2:] async for row in page]

    assert asyncio.run(run()) == (200, ["01", "02", "03", "04"])


# Dict bodies


def test_a_dict_body_is_sent_as_written():
    server = Server({("/v1/tags", None): httpx.Response(201, json=TAG)})
    with sync_for(server) as client:
        tag = client.tags.create(body={"name": "VIP", "color": "#ff0000"})
    assert isinstance(tag, Tag)
    assert json.loads(server.requests[0].read()) == {"name": "VIP", "color": "#ff0000"}
    assert server.requests[0].headers["Idempotency-Key"]


def test_a_dict_body_takes_python_values_and_nested_models():
    server = Server({("/v1/working_hours", None): httpx.Response(200, json=HOURS)})
    with sync_for(server) as client:
        client.working_hours.replace(
            body={
                "slots": [
                    WorkingHoursSlot(days=[1], start="09:00", end="13:00"),
                    {"days": (2, 3), "start": "14:00", "end": "18:00"},
                ]
            }
        )
    assert json.loads(server.requests[0].read()) == {
        "slots": [{"days": [1], "start": "09:00", "end": "13:00"}, {"days": [2, 3], "start": "14:00", "end": "18:00"}]
    }


def test_a_dict_body_sends_dates_enums_and_uuids_as_json_and_leaves_unset_out():
    rule = {
        "id": "00000000-0000-0000-0000-0000000000bb",
        "location_id": "11111111-1111-1111-1111-111111111111",
        "phone_number": "+393480000001",
        "kind": "vip",
        "label": None,
        "created_at": "2026-10-01T08:00:00+00:00",
        "updated_at": "2026-10-01T08:00:00+00:00",
    }
    server = Server(
        {
            ("/v1/caller_rules", None): httpx.Response(201, json=rule),
            ("/v1/appointments", None): httpx.Response(
                400, json={"error": {"type": "invalid_request", "code": "c", "message": "m", "request_id": "r"}}
            ),
        }
    )
    with sync_for(server) as client:
        client.caller_rules.with_raw_response.create(
            body={"phone_number": "+393480000001", "kind": CallerRuleKind.VIP, "label": UNSET}
        )
        with pytest.raises(InvalidRequestError):
            client.appointments.create(
                body={
                    "client_name": "Ada",
                    "client_surname": "Lovelace",
                    "start_at": datetime.datetime(2026, 11, 2, 9, 30, tzinfo=datetime.UTC),
                    "service_id": uuid.UUID(int=1),  # type: ignore[typeddict-item]
                }
            )
    assert json.loads(server.requests[0].read()) == {"phone_number": "+393480000001", "kind": "vip"}
    assert json.loads(server.requests[1].read()) == {
        "client_name": "Ada",
        "client_surname": "Lovelace",
        "start_at": "2026-11-02T09:30:00+00:00",
        "service_id": "00000000-0000-0000-0000-000000000001",
    }


def test_an_optional_body_is_left_out_or_sent_as_a_dict():
    pending = "00000000-0000-0000-0000-0000000000cc"
    server = Server({(f"/v1/pending_contacts/{pending}/approve", None): httpx.Response(200, json=contact(1))})
    with sync_for(server) as client:
        client.pending_contacts.approve(pending)
        client.pending_contacts.approve(pending, body={"first_name": "Ada"})
    assert server.requests[0].read() == b""
    assert json.loads(server.requests[1].read()) == {"first_name": "Ada"}


def test_every_body_model_has_a_dict_with_its_keys():
    for tag in METHODS:
        for name, value in vars(getattr(talki.api, tag)).items():
            if not (inspect.ismodule(value) and hasattr(value, "sync_detailed")):
                continue
            body = inspect.signature(value.sync_detailed).parameters.get("body")
            if body is None:
                continue
            model = typing.get_args(typing.get_type_hints(value.sync_detailed)["body"]) or (
                typing.get_type_hints(value.sync_detailed)["body"],
            )
            model = next(each for each in model if hasattr(each, "from_dict"))
            as_dict = getattr(talki.models, f"{model.__name__}Dict")
            fields = {field.name for field in attrs.fields(model) if field.name != "additional_properties"}
            assert as_dict.__annotations__.keys() == fields, model.__name__
            # `Required[…]` as written: the model modules postpone their
            # annotations, so `__required_keys__` cannot see it at runtime.
            required = {
                key
                for key, hint in as_dict.__annotations__.items()
                if str(getattr(hint, "__forward_arg__", hint)).startswith("Required[")
            }
            assert required == {
                field.name for field in attrs.fields(model) if field.default is attrs.NOTHING and field.init
            }, model.__name__


# Async lists without `await`


def test_an_async_list_is_iterated_without_await():
    server = three_pages()

    async def run() -> tuple[list[str], list[int], int]:
        async with async_for(server) as client:
            pager = client.contacts.list(limit=2)
            assert isinstance(pager, AsyncPager)
            assert server.cursors == []  # nothing sent until awaited or iterated
            rows = [row.phone_number[-2:] async for row in pager]
            sizes = [len(page.data) async for page in pager.iter_pages()]
            first = await client.contacts.list(limit=2)
            return rows, sizes, len(first.data)

    rows, sizes, first = asyncio.run(run())
    assert rows == ["01", "02", "03", "04"]
    assert sizes == [2, 1, 1]
    assert first == 2


def test_an_async_list_iterated_without_await_raises_from_the_loop():
    refused = httpx.Response(
        400, json={"error": {"type": "invalid_request", "code": "invalid_cursor", "message": "m", "request_id": "r"}}
    )

    async def run() -> None:
        async with async_for(Server({("/v1/contacts", "bad"): refused})) as client:
            pager = client.contacts.list(cursor="bad")
            with pytest.raises(InvalidRequestError):
                async for _ in pager:
                    pass

    asyncio.run(run())


# with_options


def test_with_options_changes_the_settings_for_its_calls_only():
    answers = [httpx.Response(503), httpx.Response(503), httpx.Response(200, json={"total": 7})]
    seen: list[httpx.Request] = []

    def server(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return answers[len(seen) - 1] if len(seen) <= len(answers) else answers[-1]

    client = Talki(api_key="talki_test_x", transport=httpx.MockTransport(server), timeout=30)
    client.transport._sleep = lambda delay: None
    once = client.with_options(max_retries=0, timeout=5)
    assert type(once) is Talki
    with pytest.raises(talki.ServerError):
        once.calls.count()
    assert len(seen) == 1
    # The original still retries, and keeps its timeout.
    assert client.calls.count().total == 7
    assert len(seen) == 3
    assert once.client.get_httpx_client().timeout == httpx.Timeout(5)
    assert client.client.get_httpx_client().timeout == httpx.Timeout(30)
    # One pool of connections, one token renewal, the same headers.
    assert once.transport._connections is client.transport._connections
    assert once.auth is client.auth
    assert (
        once.client.get_httpx_client().headers["User-Agent"] == client.client.get_httpx_client().headers["User-Agent"]
    )
    assert once.calls is not client.calls


def test_with_options_copies_every_setting():
    client = Talki(api_key="talki_test_x")
    assert set(vars(client)) == talki._talki._SETTINGS
    copy = client.with_options()
    assert set(vars(copy)) == talki._talki._SETTINGS
    assert copy.transport is client.transport and copy.timeout == client.timeout


def test_with_options_on_the_async_client():
    server = Server({("/v1/calls/count", None): httpx.Response(200, json={"total": 7})})

    async def run() -> int:
        async with async_for(server) as client:
            once = client.with_options(timeout=5)
            assert type(once) is AsyncTalki
            return (await once.calls.count()).total

    assert asyncio.run(run()) == 7


def test_with_options_refuses_negative_retries():
    with pytest.raises(ValueError):
        Talki(api_key="talki_test_x").with_options(max_retries=-1)
