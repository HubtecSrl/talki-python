from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_count import CallCount
from ...models.error_envelope import ErrorEnvelope
from ...models.inbox_status import InboxStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    status: InboxStatus | Unset = InboxStatus.ALL,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    params: dict[str, Any] = {}

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

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
        "url": "/v1/calls/count",
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
) -> CallCount | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = CallCount.from_dict(response.json())

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
) -> Response[CallCount | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    status: InboxStatus | Unset = InboxStatus.ALL,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[CallCount | ErrorEnvelope]:
    """Count calls

     Count the calls in one inbox view. `status=unread` is the unread badge. Requires `calls:read`.
    Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallCount | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
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
    status: InboxStatus | Unset = InboxStatus.ALL,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> CallCount | ErrorEnvelope | None:
    """Count calls

     Count the calls in one inbox view. `status=unread` is the unread badge. Requires `calls:read`.
    Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallCount | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        status=status,
        location_id=location_id,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    status: InboxStatus | Unset = InboxStatus.ALL,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[CallCount | ErrorEnvelope]:
    """Count calls

     Count the calls in one inbox view. `status=unread` is the unread badge. Requires `calls:read`.
    Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallCount | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        status=status,
        location_id=location_id,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    status: InboxStatus | Unset = InboxStatus.ALL,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> CallCount | ErrorEnvelope | None:
    """Count calls

     Count the calls in one inbox view. `status=unread` is the unread badge. Requires `calls:read`.
    Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallCount | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            status=status,
            location_id=location_id,
            talki_version=talki_version,
        )
    ).parsed
