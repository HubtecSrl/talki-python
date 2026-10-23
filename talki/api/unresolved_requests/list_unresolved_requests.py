from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.unresolved_request_list import UnresolvedRequestList
from ...models.unresolved_request_status import UnresolvedRequestStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    status: None | UnresolvedRequestStatus | Unset = UNSET,
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
    elif isinstance(status, UnresolvedRequestStatus):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    json_location_id: None | str | Unset
    if isinstance(location_id, Unset):
        json_location_id = UNSET
    else:
        json_location_id = location_id
    params["location_id"] = json_location_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/unresolved_requests",
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
) -> ErrorEnvelope | UnresolvedRequestList | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = UnresolvedRequestList.from_dict(response.json())

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
) -> Response[ErrorEnvelope | UnresolvedRequestList]:
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
    status: None | UnresolvedRequestStatus | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | UnresolvedRequestList]:
    """List unresolved-request changes

     Walk the feed of questions the assistant could not answer. A request moves again when it is closed.
    Requires `unresolved:read`. Limited to 600 requests per minute per account (API key) or per
    installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of requests to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Not interchangeable with
            another endpoint's cursor.
        status (None | UnresolvedRequestStatus | Unset): Restrict to `open`, `resolved` or
            `dismissed`. Omit to get all of them — which is what an incremental sync needs, since a
            request being closed is the change you most need to see. Use this only for a point-in-time
            snapshot of the open list.
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
        Response[ErrorEnvelope | UnresolvedRequestList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        status=status,
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
    status: None | UnresolvedRequestStatus | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | UnresolvedRequestList | None:
    """List unresolved-request changes

     Walk the feed of questions the assistant could not answer. A request moves again when it is closed.
    Requires `unresolved:read`. Limited to 600 requests per minute per account (API key) or per
    installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of requests to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Not interchangeable with
            another endpoint's cursor.
        status (None | UnresolvedRequestStatus | Unset): Restrict to `open`, `resolved` or
            `dismissed`. Omit to get all of them — which is what an incremental sync needs, since a
            request being closed is the change you most need to see. Use this only for a point-in-time
            snapshot of the open list.
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
        ErrorEnvelope | UnresolvedRequestList
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        status=status,
        location_id=location_id,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    status: None | UnresolvedRequestStatus | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | UnresolvedRequestList]:
    """List unresolved-request changes

     Walk the feed of questions the assistant could not answer. A request moves again when it is closed.
    Requires `unresolved:read`. Limited to 600 requests per minute per account (API key) or per
    installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of requests to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Not interchangeable with
            another endpoint's cursor.
        status (None | UnresolvedRequestStatus | Unset): Restrict to `open`, `resolved` or
            `dismissed`. Omit to get all of them — which is what an incremental sync needs, since a
            request being closed is the change you most need to see. Use this only for a point-in-time
            snapshot of the open list.
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
        Response[ErrorEnvelope | UnresolvedRequestList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        status=status,
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
    status: None | UnresolvedRequestStatus | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | UnresolvedRequestList | None:
    """List unresolved-request changes

     Walk the feed of questions the assistant could not answer. A request moves again when it is closed.
    Requires `unresolved:read`. Limited to 600 requests per minute per account (API key) or per
    installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of requests to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Not interchangeable with
            another endpoint's cursor.
        status (None | UnresolvedRequestStatus | Unset): Restrict to `open`, `resolved` or
            `dismissed`. Omit to get all of them — which is what an incremental sync needs, since a
            request being closed is the change you most need to see. Use this only for a point-in-time
            snapshot of the open list.
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
        ErrorEnvelope | UnresolvedRequestList
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            status=status,
            location_id=location_id,
            talki_version=talki_version,
        )
    ).parsed
