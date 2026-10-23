from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.mark_all_read_result import MarkAllReadResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    params: dict[str, Any] = {}

    json_location_id: None | str | Unset
    if isinstance(location_id, Unset):
        json_location_id = UNSET
    else:
        json_location_id = location_id
    params["location_id"] = json_location_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/calls/mark_all_read",
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
) -> ErrorEnvelope | MarkAllReadResult | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = MarkAllReadResult.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

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
) -> Response[ErrorEnvelope | MarkAllReadResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorEnvelope | MarkAllReadResult]:
    """Mark all calls read

     Mark every unread call in the inbox read. Each one sends `call.updated`. Requires `calls:write`.
    Limited to 120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for the calls of every location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | MarkAllReadResult]
    """

    kwargs = _get_kwargs(
        location_id=location_id,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> ErrorEnvelope | MarkAllReadResult | None:
    """Mark all calls read

     Mark every unread call in the inbox read. Each one sends `call.updated`. Requires `calls:write`.
    Limited to 120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for the calls of every location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | MarkAllReadResult
    """

    return sync_detailed(
        client=client,
        location_id=location_id,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorEnvelope | MarkAllReadResult]:
    """Mark all calls read

     Mark every unread call in the inbox read. Each one sends `call.updated`. Requires `calls:write`.
    Limited to 120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for the calls of every location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | MarkAllReadResult]
    """

    kwargs = _get_kwargs(
        location_id=location_id,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> ErrorEnvelope | MarkAllReadResult | None:
    """Mark all calls read

     Mark every unread call in the inbox read. Each one sends `call.updated`. Requires `calls:write`.
    Limited to 120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for the calls of every location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | MarkAllReadResult
    """

    return (
        await asyncio_detailed(
            client=client,
            location_id=location_id,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
