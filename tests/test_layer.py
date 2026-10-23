"""The hand-written part of `talki`: `Talki`, its transport, `unwrap` and the
exceptions, against an `httpx.MockTransport`."""

import asyncio
import copy
import email.utils
import gzip
import json
import pickle
import time
import uuid
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

import httpx
import pytest

import talki
from talki import (
    ApiError,
    AuthenticationError,
    ConflictError,
    InvalidRequestError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    Talki,
    TalkiError,
    unwrap,
)
from talki.api.account import get_account
from talki.api.appointments import create_appointment
from talki.api.contacts import delete_contact
from talki.api.tags import list_tags
from talki.exceptions import retry_after_seconds
from talki.models import AppointmentCreate, TagList

Handler = Callable[[httpx.Request], httpx.Response]


def envelope(status: int, type_: str, code: str, **headers: str) -> httpx.Response:
    return httpx.Response(
        status,
        json={"error": {"type": type_, "code": code, "message": "m", "request_id": "req_1"}},
        headers=headers,
    )


class Recorder:
    """The handler's answers in order, and every request it saw."""

    def __init__(self, *answers: httpx.Response | Exception) -> None:
        self.answers = list(answers)
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        answer = self.answers.pop(0) if len(self.answers) > 1 else self.answers[0]
        if isinstance(answer, Exception):
            raise answer
        return answer


def make(handler: Handler, *, sleeps: list[float] | None = None, **options) -> Talki:
    client = Talki(api_key="talki_test_x", transport=httpx.MockTransport(handler), **options)
    recorded = sleeps if sleeps is not None else []
    client.transport._sleep = recorded.append

    async def async_sleep(delay: float) -> None:
        recorded.append(delay)

    client.transport._async_sleep = async_sleep
    return client


APPOINTMENT = AppointmentCreate.from_dict(
    {"client_name": "Ada", "client_surname": "Rossi", "start_at": "2026-11-03T10:00:00+01:00"}
)


# The client itself.


def test_exactly_one_credential():
    with pytest.raises(ValueError):
        Talki()
    with pytest.raises(ValueError):
        Talki(api_key="talki_test_x", access_token="talki_at_x")


def test_the_version_defaults_to_the_one_the_package_was_generated_from():
    seen = Recorder(httpx.Response(204))
    with make(seen) as client:
        get_account.sync_detailed(client=client.client)
    assert seen.requests[0].headers["Talki-Version"] == talki.API_VERSION
    assert seen.requests[0].headers["Authorization"] == "Bearer talki_test_x"


def test_no_version_sends_none_and_an_access_token_is_a_bearer():
    seen = Recorder(httpx.Response(204))
    client = Talki(access_token="talki_at_x", version=None, transport=httpx.MockTransport(seen))
    with client:
        get_account.sync_detailed(client=client.client)
    assert "Talki-Version" not in seen.requests[0].headers
    assert seen.requests[0].headers["Authorization"] == "Bearer talki_at_x"


def test_the_repr_never_shows_the_credential():
    assert "talki_test_x" not in repr(Talki(api_key="talki_test_x"))


# Idempotency keys.


def test_a_write_without_a_key_gets_one_and_a_read_does_not():
    seen = Recorder(httpx.Response(204))
    with make(seen) as client:
        create_appointment.sync_detailed(client=client.client, body=APPOINTMENT)
        get_account.sync_detailed(client=client.client)
    key = seen.requests[0].headers["Idempotency-Key"]
    assert uuid.UUID(key)
    assert "Idempotency-Key" not in seen.requests[1].headers


def test_a_key_given_is_kept():
    seen = Recorder(httpx.Response(204))
    with make(seen) as client:
        create_appointment.sync_detailed(client=client.client, body=APPOINTMENT, idempotency_key="mine")
    assert seen.requests[0].headers["Idempotency-Key"] == "mine"


def test_auto_idempotency_off_sends_no_key():
    seen = Recorder(httpx.Response(204))
    with make(seen, auto_idempotency=False) as client:
        create_appointment.sync_detailed(client=client.client, body=APPOINTMENT)
    assert "Idempotency-Key" not in seen.requests[0].headers


# Retries.


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_a_read_is_retried_on_a_retryable_status(status):
    seen = Recorder(httpx.Response(status), httpx.Response(204))
    sleeps: list[float] = []
    with make(seen, sleeps=sleeps) as client:
        response = get_account.sync_detailed(client=client.client)
    assert response.status_code == 204
    assert len(seen.requests) == 2
    assert len(sleeps) == 1 and 0.25 <= sleeps[0] <= 0.5


def test_retry_after_is_honoured():
    seen = Recorder(
        envelope(429, "rate_limit_error", "rate_limit_exceeded", **{"Retry-After": "3"}), httpx.Response(204)
    )
    sleeps: list[float] = []
    with make(seen, sleeps=sleeps) as client:
        get_account.sync_detailed(client=client.client)
    assert sleeps == [3.0]


def test_a_long_retry_after_is_handed_back():
    seen = Recorder(envelope(429, "rate_limit_error", "rate_limit_exceeded", **{"Retry-After": "120"}))
    with make(seen) as client:
        with pytest.raises(RateLimitError) as raised:
            unwrap(get_account.sync_detailed(client=client.client))
    assert len(seen.requests) == 1
    assert raised.value.retry_after == 120.0


def test_a_write_is_retried_with_the_same_key():
    seen = Recorder(httpx.Response(503), httpx.Response(204))
    with make(seen) as client:
        create_appointment.sync_detailed(client=client.client, body=APPOINTMENT)
    keys = [request.headers["Idempotency-Key"] for request in seen.requests]
    assert len(keys) == 2 and keys[0] == keys[1]
    assert seen.requests[0].content == seen.requests[1].content


def test_a_write_without_a_key_is_never_retried():
    seen = Recorder(httpx.Response(503), httpx.Response(204))
    with make(seen, auto_idempotency=False) as client:
        response = create_appointment.sync_detailed(client=client.client, body=APPOINTMENT)
    assert response.status_code == 503
    assert len(seen.requests) == 1


def test_retries_stop_at_max_retries():
    seen = Recorder(envelope(503, "api_error", "service_unavailable"))
    with make(seen, max_retries=3) as client:
        with pytest.raises(ServerError):
            unwrap(get_account.sync_detailed(client=client.client))
    assert len(seen.requests) == 4


def test_max_retries_zero_never_retries():
    seen = Recorder(httpx.Response(503), httpx.Response(204))
    with make(seen, max_retries=0) as client:
        assert get_account.sync_detailed(client=client.client).status_code == 503
    assert len(seen.requests) == 1


def test_request_in_progress_is_retried_and_another_conflict_is_not():
    seen = Recorder(envelope(409, "conflict", "request_in_progress"), httpx.Response(204))
    with make(seen) as client:
        assert create_appointment.sync_detailed(client=client.client, body=APPOINTMENT).status_code == 204
    assert len(seen.requests) == 2

    other = Recorder(envelope(409, "conflict", "slot_unavailable"), httpx.Response(204))
    with make(other) as client:
        with pytest.raises(ConflictError) as raised:
            unwrap(create_appointment.sync_detailed(client=client.client, body=APPOINTMENT))
    assert raised.value.code == "slot_unavailable"
    assert len(other.requests) == 1


def test_a_connection_never_made_is_retried_even_for_a_write_without_a_key():
    seen = Recorder(httpx.ConnectError("refused"), httpx.Response(204))
    with make(seen, auto_idempotency=False) as client:
        assert create_appointment.sync_detailed(client=client.client, body=APPOINTMENT).status_code == 204
    assert len(seen.requests) == 2


def test_a_timeout_after_sending_is_retried_for_a_read_only():
    seen = Recorder(httpx.ReadTimeout("slow"), httpx.Response(204))
    with make(seen) as client:
        assert get_account.sync_detailed(client=client.client).status_code == 204
    assert len(seen.requests) == 2

    keyed = Recorder(httpx.ReadTimeout("slow"), httpx.Response(204))
    with make(keyed) as client:
        with pytest.raises(httpx.ReadTimeout) as raised:
            create_appointment.sync_detailed(client=client.client, body=APPOINTMENT, idempotency_key="k1")
    assert len(keyed.requests) == 1
    # The key sent is on the error, to retry with once the outcome is known.
    assert raised.value.request.headers["Idempotency-Key"] == "k1"


def test_the_async_client_retries_and_adds_keys_too():
    seen = Recorder(httpx.Response(502), httpx.Response(204))
    sleeps: list[float] = []

    async def run() -> int:
        async with make(seen, sleeps=sleeps) as client:
            response = await create_appointment.asyncio_detailed(client=client.client, body=APPOINTMENT)
        return int(response.status_code)

    assert asyncio.run(run()) == 204
    assert len(sleeps) == 1
    assert seen.requests[0].headers["Idempotency-Key"] == seen.requests[1].headers["Idempotency-Key"]


# unwrap and the exceptions.


@pytest.mark.parametrize(
    ("status", "type_", "expected"),
    [
        (400, "invalid_request", InvalidRequestError),
        (401, "authentication_error", AuthenticationError),
        (403, "permission_error", PermissionDeniedError),
        (409, "conflict", ConflictError),
        (429, "rate_limit_error", RateLimitError),
        (500, "api_error", ServerError),
        (403, "type_added_later", ApiError),
    ],
)
def test_unwrap_raises_the_class_of_the_error_type(status, type_, expected):
    seen = Recorder(envelope(status, type_, "some_code"))
    with make(seen, max_retries=0) as client:
        with pytest.raises(expected) as raised:
            unwrap(get_account.sync_detailed(client=client.client))
    error = raised.value
    assert type(error) is expected
    assert isinstance(error, TalkiError)
    assert (error.status, error.type, error.code, error.request_id) == (status, type_, "some_code", "req_1")


def test_an_error_without_an_envelope_is_read_by_its_status():
    seen = Recorder(httpx.Response(502, text="<html>Bad gateway</html>", headers={"content-type": "text/html"}))
    with make(seen, max_retries=0) as client:
        response = get_account.sync_detailed(client=client.client)
        with pytest.raises(ServerError) as raised:
            unwrap(response)
    assert response.parsed is None
    assert raised.value.code is None
    assert "Bad gateway" in raised.value.message


def test_an_html_500_on_an_operation_that_declares_500_is_not_a_decode_error():
    seen = Recorder(httpx.Response(500, text="<html>oops</html>", headers={"content-type": "text/html"}))
    with make(seen, max_retries=0) as client:
        response = get_account.sync_detailed(client=client.client)
    assert response.parsed is None
    with pytest.raises(ServerError):
        unwrap(response)


def test_unwrap_returns_none_for_no_content():
    seen = Recorder(httpx.Response(204))
    with make(seen) as client:
        assert unwrap(delete_contact.sync_detailed("c", client=client.client)) is None


def test_unwrap_refuses_a_success_it_cannot_read():
    seen = Recorder(httpx.Response(202, json={"unexpected": True}))
    with make(seen) as client:
        with pytest.raises(ApiError) as raised:
            unwrap(get_account.sync_detailed(client=client.client))
    assert raised.value.status == 202


def test_unwrap_returns_the_model():
    seen = Recorder(httpx.Response(200, json={"object": "list", "data": [], "has_more": False, "next_cursor": None}))
    with make(seen) as client:
        tags = unwrap(list_tags.sync_detailed(client=client.client))
    assert isinstance(tags, TagList)
    assert tags.data == []


# What a write is not retried on, and the edges of the transport.


def test_a_write_the_api_failed_is_not_retried():
    for answer in (
        envelope(500, "api_error", "internal_error"),
        envelope(503, "api_error", "service_unavailable"),
    ):
        seen = Recorder(answer, httpx.Response(204))
        with make(seen) as client:
            with pytest.raises(ServerError):
                unwrap(create_appointment.sync_detailed(client=client.client, body=APPOINTMENT))
        assert len(seen.requests) == 1


def test_a_write_a_gateway_failed_is_retried():
    gateway = httpx.Response(502, text="<html>Bad gateway</html>", headers={"content-type": "text/html"})
    seen = Recorder(gateway, httpx.Response(204))
    with make(seen) as client:
        assert create_appointment.sync_detailed(client=client.client, body=APPOINTMENT).status_code == 204
    assert len(seen.requests) == 2


def test_a_429_is_retried_even_for_a_write_without_a_key():
    seen = Recorder(envelope(429, "rate_limit_error", "rate_limit_exceeded"), httpx.Response(204))
    with make(seen, auto_idempotency=False) as client:
        assert create_appointment.sync_detailed(client=client.client, body=APPOINTMENT).status_code == 204
    assert len(seen.requests) == 2


def test_a_blank_key_is_replaced_and_never_trusted():
    seen = Recorder(httpx.Response(204))
    with make(seen) as client:
        create_appointment.sync_detailed(client=client.client, body=APPOINTMENT, idempotency_key="  ")
    assert uuid.UUID(seen.requests[0].headers["Idempotency-Key"])

    unkeyed = Recorder(httpx.Response(502), httpx.Response(204))
    with make(unkeyed, auto_idempotency=False) as client:
        response = create_appointment.sync_detailed(client=client.client, body=APPOINTMENT, idempotency_key="")
    assert response.status_code == 502
    assert len(unkeyed.requests) == 1
    assert "Idempotency-Key" not in unkeyed.requests[0].headers


def test_a_pool_timeout_was_never_sent_and_is_retried():
    seen = Recorder(httpx.PoolTimeout("busy"), httpx.Response(204))
    with make(seen, auto_idempotency=False) as client:
        assert create_appointment.sync_detailed(client=client.client, body=APPOINTMENT).status_code == 204


def test_retry_after_as_a_date():
    when = email.utils.format_datetime(datetime.now(UTC) + timedelta(seconds=30), usegmt=True)
    seen = Recorder(httpx.Response(503, headers={"Retry-After": when}), httpx.Response(204))
    sleeps: list[float] = []
    with make(seen, sleeps=sleeps) as client:
        get_account.sync_detailed(client=client.client)
    assert len(sleeps) == 1 and 25 <= sleeps[0] <= 31


def test_retry_after_as_a_date_without_a_zone_is_utc(monkeypatch):
    """`-0000` parses to a naive datetime, which `.timestamp()` would read in
    local time: hours off anywhere but UTC."""
    monkeypatch.setenv("TZ", "America/New_York")
    time.tzset()
    try:
        later = datetime.now(UTC).replace(tzinfo=None) + timedelta(seconds=30)
        when = email.utils.format_datetime(later)
        assert when.endswith("-0000")
        assert 25 <= retry_after_seconds({"Retry-After": when}) <= 31
    finally:
        monkeypatch.undo()
        time.tzset()


def test_a_409_read_for_its_code_is_still_a_whole_response():
    body = json.dumps({"error": {"type": "conflict", "code": "slot_unavailable", "message": "m", "request_id": "r"}})
    streamed = httpx.Response(409, stream=httpx.ByteStream(body.encode()), headers={"content-type": "application/json"})
    seen = Recorder(streamed)
    with make(seen) as client:
        response = client.client.get_httpx_client().post("/v1/appointments", json={})
    assert response.status_code == 409
    assert response.elapsed.total_seconds() >= 0
    assert response.json()["error"]["code"] == "slot_unavailable"


def test_the_async_client_waits_out_a_request_in_progress():
    seen = Recorder(envelope(409, "conflict", "request_in_progress"), httpx.Response(204))

    async def run() -> int:
        async with make(seen) as client:
            response = await create_appointment.asyncio_detailed(client=client.client, body=APPOINTMENT)
        return int(response.status_code)

    assert asyncio.run(run()) == 204
    assert len(seen.requests) == 2


def test_a_transport_for_one_mode_refuses_the_other():
    class SyncOnly(httpx.BaseTransport):
        def handle_request(self, request: httpx.Request) -> httpx.Response:
            return httpx.Response(204)

    client = Talki(api_key="talki_test_x", transport=SyncOnly())

    async def run() -> None:
        async with client:
            await get_account.asyncio_detailed(client=client.client)

    with pytest.raises(TypeError):
        asyncio.run(run())


def test_an_error_survives_pickle_and_copy():
    error = RateLimitError(status=429, code="rate_limit_exceeded", message="m", headers={"Retry-After": "3"})
    for clone in (pickle.loads(pickle.dumps(error)), copy.copy(error), copy.deepcopy(error)):
        assert type(clone) is RateLimitError
        assert (clone.status, clone.code, clone.retry_after) == (429, "rate_limit_exceeded", 3.0)


def test_the_maintenance_page_is_retried_for_a_write_and_read_as_no_envelope():
    maintenance = httpx.Response(503, json={"error": "maintenance", "message": "back soon"})
    seen = Recorder(maintenance, httpx.Response(204))
    with make(seen) as client:
        assert create_appointment.sync_detailed(client=client.client, body=APPOINTMENT).status_code == 204
    assert len(seen.requests) == 2

    # The one operation declaring 503 reads it as undeclared rather than failing.
    from talki.api.account import start_forwarding_check

    down = Recorder(maintenance)
    with make(down, max_retries=0) as client:
        response = start_forwarding_check.sync_detailed(client=client.client)
    assert response.parsed is None
    with pytest.raises(ServerError):
        unwrap(response)


def test_a_compressed_answer_read_here_is_still_decoded_once():
    body = json.dumps({"error": {"type": "conflict", "code": "slot_unavailable", "message": "m", "request_id": "r"}})
    # Streamed, as a real transport answers, not built already read.
    compressed = httpx.Response(
        409,
        stream=httpx.ByteStream(gzip.compress(body.encode())),
        headers={"content-type": "application/json", "content-encoding": "gzip"},
    )
    seen = Recorder(compressed)
    with make(seen) as client:
        with pytest.raises(ConflictError) as raised:
            unwrap(create_appointment.sync_detailed(client=client.client, body=APPOINTMENT))
    assert raised.value.code == "slot_unavailable"


def test_retry_after_survives_pickle_with_real_headers():
    headers = httpx.Headers(
        [(b"Retry-After", b"7"), (b"X-Proxy", "é".encode()), (b"Set-Cookie", b"a=1"), (b"Set-Cookie", b"b=2")]
    )
    error = RateLimitError(status=429, headers=headers)
    for clone in (pickle.loads(pickle.dumps(error)), copy.copy(error)):
        assert clone.retry_after == 7.0
        assert clone.headers.get_list("set-cookie") == ["a=1", "b=2"]
    assert RateLimitError(status=429, headers={"retry-after": "2", "X": "é"}).retry_after == 2.0


def test_a_proxy_is_given_to_the_transport_httpx_builds():
    client = Talki(api_key="talki_test_x", proxy="http://proxy.example:3128")
    inner = client.transport._sync_transport()
    assert isinstance(inner, httpx.HTTPTransport)
    proxy = client.transport._proxy_config()
    assert proxy is not None and proxy.url == httpx.URL("http://proxy.example:3128")
