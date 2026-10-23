import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_list import CallList
from ...models.call_outcome import CallOutcome
from ...models.error_envelope import ErrorEnvelope
from ...models.inbox_status import InboxStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    sync: bool | Unset = False,
    created_after: datetime.datetime | None | Unset = UNSET,
    created_before: datetime.datetime | None | Unset = UNSET,
    status: InboxStatus | Unset = InboxStatus.ALL,
    phone: None | str | Unset = UNSET,
    contact_id: None | str | Unset = UNSET,
    q: None | str | Unset = UNSET,
    outcome: CallOutcome | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    params: dict[str, Any] = {}

    params["limit"] = limit

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    params["sync"] = sync

    json_created_after: None | str | Unset
    if isinstance(created_after, Unset):
        json_created_after = UNSET
    elif isinstance(created_after, datetime.datetime):
        json_created_after = created_after.isoformat()
    else:
        json_created_after = created_after
    params["created_after"] = json_created_after

    json_created_before: None | str | Unset
    if isinstance(created_before, Unset):
        json_created_before = UNSET
    elif isinstance(created_before, datetime.datetime):
        json_created_before = created_before.isoformat()
    else:
        json_created_before = created_before
    params["created_before"] = json_created_before

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    json_phone: None | str | Unset
    if isinstance(phone, Unset):
        json_phone = UNSET
    else:
        json_phone = phone
    params["phone"] = json_phone

    json_contact_id: None | str | Unset
    if isinstance(contact_id, Unset):
        json_contact_id = UNSET
    else:
        json_contact_id = contact_id
    params["contact_id"] = json_contact_id

    json_q: None | str | Unset
    if isinstance(q, Unset):
        json_q = UNSET
    else:
        json_q = q
    params["q"] = json_q

    json_outcome: None | str | Unset
    if isinstance(outcome, Unset):
        json_outcome = UNSET
    elif isinstance(outcome, CallOutcome):
        json_outcome = outcome.value
    else:
        json_outcome = outcome
    params["outcome"] = json_outcome

    json_location_id: None | str | Unset
    if isinstance(location_id, Unset):
        json_location_id = UNSET
    else:
        json_location_id = location_id
    params["location_id"] = json_location_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/calls",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _is_envelope(response: httpx.Response) -> bool:
    """Whether an error answer is the API's `{"error": {…}}`."""
    if "json" not in response.headers.get("content-type", ""):
        return False
    try:
        body = response.json()
    except ValueError:
        return False
    return isinstance(body, dict) and isinstance(body.get("error"), dict)


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CallList | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = CallList.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorEnvelope.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = ErrorEnvelope.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ErrorEnvelope.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CallList | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    sync: bool | Unset = False,
    created_after: datetime.datetime | None | Unset = UNSET,
    created_before: datetime.datetime | None | Unset = UNSET,
    status: InboxStatus | Unset = InboxStatus.ALL,
    phone: None | str | Unset = UNSET,
    contact_id: None | str | Unset = UNSET,
    q: None | str | Unset = UNSET,
    outcome: CallOutcome | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[CallList | ErrorEnvelope]:
    """List calls

     Read the newest-first call log, or set `sync=true` for a resumable change feed. Search the log with
    `phone`, `contact_id`, `q` or `outcome`; they do not combine with `sync=true`. Requires
    `calls:read`. Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of calls to return. Default: 50.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page. A cursor works only in the mode that issued it (`sync=true` or the
            default list); a cursor from the other mode is refused.
        sync (bool | Unset): Switch to the CHANGE FEED: ordered by when each record was committed,
            not by when the call started, and resumable exactly like `GET /v1/appointments`. This is
            how a system keeping its own copy recovers from missed webhooks — store `next_cursor`,
            which is returned on the last page too, and drive the loop from `has_more`. Leave it off
            for the newest-first list a person reads. Default: False.
        created_after (datetime.datetime | None | Unset): Only calls recorded at or after this
            instant (RFC 3339 UTC). Inclusive: a call at exactly this instant is returned, so dedupe
            on `id`. Filters on `created_at`, not `started_at` (see `Call.created_at`). Use it for
            reporting windows, not as a sync watermark: a timestamp watermark can skip a call
            permanently. Use `sync=true` to resume a sync; the two cannot be combined.
        created_before (datetime.datetime | None | Unset): Only calls recorded strictly before
            this instant (RFC 3339 UTC).
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        phone (None | str | Unset): Only calls from this number: E.164, or a national number read
            as Italian. Not with `sync=true`.
        contact_id (None | str | Unset): Only calls from this contact's number
            (`caller.contact_id`). Not with `sync=true`.
        q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
            contains it, or whose caller's `display_name` does. A name that is not published as
            `display_name` is not searched either. Not with `sync=true`.
        outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
            `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
            outcomes were tracked have none and match no value. Not with `sync=true`.
        location_id (None | str | Unset): Only the records of this location, an id from `GET
            /v1/locations` (inactive ones included). Omit for every location: each record carries its
            `location_id`. Allowed on the change feed, because a record never changes location; a
            cursor is then bound to the location it was issued for, and refused with `invalid_cursor`
            under another `location_id` or without one.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallList | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        sync=sync,
        created_after=created_after,
        created_before=created_before,
        status=status,
        phone=phone,
        contact_id=contact_id,
        q=q,
        outcome=outcome,
        location_id=location_id,
        talki_version=talki_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    sync: bool | Unset = False,
    created_after: datetime.datetime | None | Unset = UNSET,
    created_before: datetime.datetime | None | Unset = UNSET,
    status: InboxStatus | Unset = InboxStatus.ALL,
    phone: None | str | Unset = UNSET,
    contact_id: None | str | Unset = UNSET,
    q: None | str | Unset = UNSET,
    outcome: CallOutcome | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> CallList | ErrorEnvelope | None:
    """List calls

     Read the newest-first call log, or set `sync=true` for a resumable change feed. Search the log with
    `phone`, `contact_id`, `q` or `outcome`; they do not combine with `sync=true`. Requires
    `calls:read`. Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of calls to return. Default: 50.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page. A cursor works only in the mode that issued it (`sync=true` or the
            default list); a cursor from the other mode is refused.
        sync (bool | Unset): Switch to the CHANGE FEED: ordered by when each record was committed,
            not by when the call started, and resumable exactly like `GET /v1/appointments`. This is
            how a system keeping its own copy recovers from missed webhooks — store `next_cursor`,
            which is returned on the last page too, and drive the loop from `has_more`. Leave it off
            for the newest-first list a person reads. Default: False.
        created_after (datetime.datetime | None | Unset): Only calls recorded at or after this
            instant (RFC 3339 UTC). Inclusive: a call at exactly this instant is returned, so dedupe
            on `id`. Filters on `created_at`, not `started_at` (see `Call.created_at`). Use it for
            reporting windows, not as a sync watermark: a timestamp watermark can skip a call
            permanently. Use `sync=true` to resume a sync; the two cannot be combined.
        created_before (datetime.datetime | None | Unset): Only calls recorded strictly before
            this instant (RFC 3339 UTC).
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        phone (None | str | Unset): Only calls from this number: E.164, or a national number read
            as Italian. Not with `sync=true`.
        contact_id (None | str | Unset): Only calls from this contact's number
            (`caller.contact_id`). Not with `sync=true`.
        q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
            contains it, or whose caller's `display_name` does. A name that is not published as
            `display_name` is not searched either. Not with `sync=true`.
        outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
            `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
            outcomes were tracked have none and match no value. Not with `sync=true`.
        location_id (None | str | Unset): Only the records of this location, an id from `GET
            /v1/locations` (inactive ones included). Omit for every location: each record carries its
            `location_id`. Allowed on the change feed, because a record never changes location; a
            cursor is then bound to the location it was issued for, and refused with `invalid_cursor`
            under another `location_id` or without one.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallList | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        sync=sync,
        created_after=created_after,
        created_before=created_before,
        status=status,
        phone=phone,
        contact_id=contact_id,
        q=q,
        outcome=outcome,
        location_id=location_id,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    sync: bool | Unset = False,
    created_after: datetime.datetime | None | Unset = UNSET,
    created_before: datetime.datetime | None | Unset = UNSET,
    status: InboxStatus | Unset = InboxStatus.ALL,
    phone: None | str | Unset = UNSET,
    contact_id: None | str | Unset = UNSET,
    q: None | str | Unset = UNSET,
    outcome: CallOutcome | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[CallList | ErrorEnvelope]:
    """List calls

     Read the newest-first call log, or set `sync=true` for a resumable change feed. Search the log with
    `phone`, `contact_id`, `q` or `outcome`; they do not combine with `sync=true`. Requires
    `calls:read`. Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of calls to return. Default: 50.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page. A cursor works only in the mode that issued it (`sync=true` or the
            default list); a cursor from the other mode is refused.
        sync (bool | Unset): Switch to the CHANGE FEED: ordered by when each record was committed,
            not by when the call started, and resumable exactly like `GET /v1/appointments`. This is
            how a system keeping its own copy recovers from missed webhooks — store `next_cursor`,
            which is returned on the last page too, and drive the loop from `has_more`. Leave it off
            for the newest-first list a person reads. Default: False.
        created_after (datetime.datetime | None | Unset): Only calls recorded at or after this
            instant (RFC 3339 UTC). Inclusive: a call at exactly this instant is returned, so dedupe
            on `id`. Filters on `created_at`, not `started_at` (see `Call.created_at`). Use it for
            reporting windows, not as a sync watermark: a timestamp watermark can skip a call
            permanently. Use `sync=true` to resume a sync; the two cannot be combined.
        created_before (datetime.datetime | None | Unset): Only calls recorded strictly before
            this instant (RFC 3339 UTC).
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        phone (None | str | Unset): Only calls from this number: E.164, or a national number read
            as Italian. Not with `sync=true`.
        contact_id (None | str | Unset): Only calls from this contact's number
            (`caller.contact_id`). Not with `sync=true`.
        q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
            contains it, or whose caller's `display_name` does. A name that is not published as
            `display_name` is not searched either. Not with `sync=true`.
        outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
            `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
            outcomes were tracked have none and match no value. Not with `sync=true`.
        location_id (None | str | Unset): Only the records of this location, an id from `GET
            /v1/locations` (inactive ones included). Omit for every location: each record carries its
            `location_id`. Allowed on the change feed, because a record never changes location; a
            cursor is then bound to the location it was issued for, and refused with `invalid_cursor`
            under another `location_id` or without one.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallList | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        sync=sync,
        created_after=created_after,
        created_before=created_before,
        status=status,
        phone=phone,
        contact_id=contact_id,
        q=q,
        outcome=outcome,
        location_id=location_id,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    sync: bool | Unset = False,
    created_after: datetime.datetime | None | Unset = UNSET,
    created_before: datetime.datetime | None | Unset = UNSET,
    status: InboxStatus | Unset = InboxStatus.ALL,
    phone: None | str | Unset = UNSET,
    contact_id: None | str | Unset = UNSET,
    q: None | str | Unset = UNSET,
    outcome: CallOutcome | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> CallList | ErrorEnvelope | None:
    """List calls

     Read the newest-first call log, or set `sync=true` for a resumable change feed. Search the log with
    `phone`, `contact_id`, `q` or `outcome`; they do not combine with `sync=true`. Requires
    `calls:read`. Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of calls to return. Default: 50.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page. A cursor works only in the mode that issued it (`sync=true` or the
            default list); a cursor from the other mode is refused.
        sync (bool | Unset): Switch to the CHANGE FEED: ordered by when each record was committed,
            not by when the call started, and resumable exactly like `GET /v1/appointments`. This is
            how a system keeping its own copy recovers from missed webhooks — store `next_cursor`,
            which is returned on the last page too, and drive the loop from `has_more`. Leave it off
            for the newest-first list a person reads. Default: False.
        created_after (datetime.datetime | None | Unset): Only calls recorded at or after this
            instant (RFC 3339 UTC). Inclusive: a call at exactly this instant is returned, so dedupe
            on `id`. Filters on `created_at`, not `started_at` (see `Call.created_at`). Use it for
            reporting windows, not as a sync watermark: a timestamp watermark can skip a call
            permanently. Use `sync=true` to resume a sync; the two cannot be combined.
        created_before (datetime.datetime | None | Unset): Only calls recorded strictly before
            this instant (RFC 3339 UTC).
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        phone (None | str | Unset): Only calls from this number: E.164, or a national number read
            as Italian. Not with `sync=true`.
        contact_id (None | str | Unset): Only calls from this contact's number
            (`caller.contact_id`). Not with `sync=true`.
        q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
            contains it, or whose caller's `display_name` does. A name that is not published as
            `display_name` is not searched either. Not with `sync=true`.
        outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
            `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
            outcomes were tracked have none and match no value. Not with `sync=true`.
        location_id (None | str | Unset): Only the records of this location, an id from `GET
            /v1/locations` (inactive ones included). Omit for every location: each record carries its
            `location_id`. Allowed on the change feed, because a record never changes location; a
            cursor is then bound to the location it was issued for, and refused with `invalid_cursor`
            under another `location_id` or without one.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallList | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            sync=sync,
            created_after=created_after,
            created_before=created_before,
            status=status,
            phone=phone,
            contact_id=contact_id,
            q=q,
            outcome=outcome,
            location_id=location_id,
            talki_version=talki_version,
        )
    ).parsed
