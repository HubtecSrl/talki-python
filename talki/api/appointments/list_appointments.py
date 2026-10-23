import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.appointment_list import AppointmentList
from ...models.appointment_status import AppointmentStatus
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    status: AppointmentStatus | None | Unset = UNSET,
    starts_after: datetime.datetime | None | Unset = UNSET,
    starts_before: datetime.datetime | None | Unset = UNSET,
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

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, AppointmentStatus):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    json_starts_after: None | str | Unset
    if isinstance(starts_after, Unset):
        json_starts_after = UNSET
    elif isinstance(starts_after, datetime.datetime):
        json_starts_after = starts_after.isoformat()
    else:
        json_starts_after = starts_after
    params["starts_after"] = json_starts_after

    json_starts_before: None | str | Unset
    if isinstance(starts_before, Unset):
        json_starts_before = UNSET
    elif isinstance(starts_before, datetime.datetime):
        json_starts_before = starts_before.isoformat()
    else:
        json_starts_before = starts_before
    params["starts_before"] = json_starts_before

    json_location_id: None | str | Unset
    if isinstance(location_id, Unset):
        json_location_id = UNSET
    else:
        json_location_id = location_id
    params["location_id"] = json_location_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/appointments",
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
) -> AppointmentList | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = AppointmentList.from_dict(response.json())

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
) -> Response[AppointmentList | ErrorEnvelope]:
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
    status: AppointmentStatus | None | Unset = UNSET,
    starts_after: datetime.datetime | None | Unset = UNSET,
    starts_before: datetime.datetime | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[AppointmentList | ErrorEnvelope]:
    """List appointment changes

     Walk the appointment change feed in commit order. Store `next_cursor` even on the last non-empty
    page. Requires `appointments:read`. Limited to 600 requests per minute per account (API key) or per
    installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of appointments to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Store the last one you
            received: it is how you resume a sync without re-reading everything. Not interchangeable
            with a `GET /v1/calls` cursor.
        status (AppointmentStatus | None | Unset): Restrict to `active` or `cancelled`. Omit to
            get both — which is what an incremental sync needs, since a cancellation is a change you
            must see. Use this only for a point-in-time snapshot.
        starts_after (datetime.datetime | None | Unset): Only appointments starting at or after
            this instant (RFC 3339 UTC). A filter on WHEN THE BOOKING IS, not on when it changed; it
            does not affect ordering and must not be used as a sync watermark.
        starts_before (datetime.datetime | None | Unset): Only appointments starting strictly
            before this instant (RFC 3339 UTC).
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
        Response[AppointmentList | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        status=status,
        starts_after=starts_after,
        starts_before=starts_before,
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
    status: AppointmentStatus | None | Unset = UNSET,
    starts_after: datetime.datetime | None | Unset = UNSET,
    starts_before: datetime.datetime | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> AppointmentList | ErrorEnvelope | None:
    """List appointment changes

     Walk the appointment change feed in commit order. Store `next_cursor` even on the last non-empty
    page. Requires `appointments:read`. Limited to 600 requests per minute per account (API key) or per
    installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of appointments to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Store the last one you
            received: it is how you resume a sync without re-reading everything. Not interchangeable
            with a `GET /v1/calls` cursor.
        status (AppointmentStatus | None | Unset): Restrict to `active` or `cancelled`. Omit to
            get both — which is what an incremental sync needs, since a cancellation is a change you
            must see. Use this only for a point-in-time snapshot.
        starts_after (datetime.datetime | None | Unset): Only appointments starting at or after
            this instant (RFC 3339 UTC). A filter on WHEN THE BOOKING IS, not on when it changed; it
            does not affect ordering and must not be used as a sync watermark.
        starts_before (datetime.datetime | None | Unset): Only appointments starting strictly
            before this instant (RFC 3339 UTC).
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
        AppointmentList | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        status=status,
        starts_after=starts_after,
        starts_before=starts_before,
        location_id=location_id,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    status: AppointmentStatus | None | Unset = UNSET,
    starts_after: datetime.datetime | None | Unset = UNSET,
    starts_before: datetime.datetime | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[AppointmentList | ErrorEnvelope]:
    """List appointment changes

     Walk the appointment change feed in commit order. Store `next_cursor` even on the last non-empty
    page. Requires `appointments:read`. Limited to 600 requests per minute per account (API key) or per
    installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of appointments to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Store the last one you
            received: it is how you resume a sync without re-reading everything. Not interchangeable
            with a `GET /v1/calls` cursor.
        status (AppointmentStatus | None | Unset): Restrict to `active` or `cancelled`. Omit to
            get both — which is what an incremental sync needs, since a cancellation is a change you
            must see. Use this only for a point-in-time snapshot.
        starts_after (datetime.datetime | None | Unset): Only appointments starting at or after
            this instant (RFC 3339 UTC). A filter on WHEN THE BOOKING IS, not on when it changed; it
            does not affect ordering and must not be used as a sync watermark.
        starts_before (datetime.datetime | None | Unset): Only appointments starting strictly
            before this instant (RFC 3339 UTC).
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
        Response[AppointmentList | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        status=status,
        starts_after=starts_after,
        starts_before=starts_before,
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
    status: AppointmentStatus | None | Unset = UNSET,
    starts_after: datetime.datetime | None | Unset = UNSET,
    starts_before: datetime.datetime | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> AppointmentList | ErrorEnvelope | None:
    """List appointment changes

     Walk the appointment change feed in commit order. Store `next_cursor` even on the last non-empty
    page. Requires `appointments:read`. Limited to 600 requests per minute per account (API key) or per
    installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of appointments to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Store the last one you
            received: it is how you resume a sync without re-reading everything. Not interchangeable
            with a `GET /v1/calls` cursor.
        status (AppointmentStatus | None | Unset): Restrict to `active` or `cancelled`. Omit to
            get both — which is what an incremental sync needs, since a cancellation is a change you
            must see. Use this only for a point-in-time snapshot.
        starts_after (datetime.datetime | None | Unset): Only appointments starting at or after
            this instant (RFC 3339 UTC). A filter on WHEN THE BOOKING IS, not on when it changed; it
            does not affect ordering and must not be used as a sync watermark.
        starts_before (datetime.datetime | None | Unset): Only appointments starting strictly
            before this instant (RFC 3339 UTC).
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
        AppointmentList | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            status=status,
            starts_after=starts_after,
            starts_before=starts_before,
            location_id=location_id,
            talki_version=talki_version,
        )
    ).parsed
