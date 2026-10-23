from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.contact_list import ContactList
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
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

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/contacts",
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
) -> ContactList | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = ContactList.from_dict(response.json())

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
) -> Response[ContactList | ErrorEnvelope]:
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
    talki_version: str | Unset = UNSET,
) -> Response[ContactList | ErrorEnvelope]:
    """List contact changes

     Walk the curated-contact change feed in commit order. Requires `contacts:read`. Limited to 600
    requests per minute per account (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of contacts to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Store the last one you
            received: it is how you resume a sync without re-reading the whole address book. Not
            interchangeable with another endpoint's cursor.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ContactList | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
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
    talki_version: str | Unset = UNSET,
) -> ContactList | ErrorEnvelope | None:
    """List contact changes

     Walk the curated-contact change feed in commit order. Requires `contacts:read`. Limited to 600
    requests per minute per account (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of contacts to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Store the last one you
            received: it is how you resume a sync without re-reading the whole address book. Not
            interchangeable with another endpoint's cursor.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ContactList | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ContactList | ErrorEnvelope]:
    """List contact changes

     Walk the curated-contact change feed in commit order. Requires `contacts:read`. Limited to 600
    requests per minute per account (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of contacts to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Store the last one you
            received: it is how you resume a sync without re-reading the whole address book. Not
            interchangeable with another endpoint's cursor.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ContactList | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ContactList | ErrorEnvelope | None:
    """List contact changes

     Walk the curated-contact change feed in commit order. Requires `contacts:read`. Limited to 600
    requests per minute per account (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of contacts to return. Default: 50.
        cursor (None | str | Unset): Opaque position in the change feed, from a previous
            response's `next_cursor`. Omit to start from the beginning. Store the last one you
            received: it is how you resume a sync without re-reading the whole address book. Not
            interchangeable with another endpoint's cursor.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ContactList | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            talki_version=talki_version,
        )
    ).parsed
