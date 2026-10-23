from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.service import Service
from ...models.service_update import ServiceUpdate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: str,
    *,
    body: ServiceUpdate,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/services/{service_id}".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

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
) -> ErrorEnvelope | Service | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = Service.from_dict(response.json())

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
) -> Response[ErrorEnvelope | Service]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: str,
    *,
    client: AuthenticatedClient,
    body: ServiceUpdate,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorEnvelope | Service]:
    """Update a service

     Update a service's name, description, price, duration or active state; omitted fields stay
    unchanged. Requires `services:write`. Limited to 120 requests per minute per account (API key) or
    per installation (OAuth).

    Args:
        service_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (ServiceUpdate): The service fields you can change. Every field is optional; an
            omitted one is left unchanged. Everything else on a service — booking mode, stay rules,
            quantities, capacity — is read-only here.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | Service]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    *,
    client: AuthenticatedClient,
    body: ServiceUpdate,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> ErrorEnvelope | Service | None:
    """Update a service

     Update a service's name, description, price, duration or active state; omitted fields stay
    unchanged. Requires `services:write`. Limited to 120 requests per minute per account (API key) or
    per installation (OAuth).

    Args:
        service_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (ServiceUpdate): The service fields you can change. Every field is optional; an
            omitted one is left unchanged. Everything else on a service — booking mode, stay rules,
            quantities, capacity — is read-only here.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | Service
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    *,
    client: AuthenticatedClient,
    body: ServiceUpdate,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorEnvelope | Service]:
    """Update a service

     Update a service's name, description, price, duration or active state; omitted fields stay
    unchanged. Requires `services:write`. Limited to 120 requests per minute per account (API key) or
    per installation (OAuth).

    Args:
        service_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (ServiceUpdate): The service fields you can change. Every field is optional; an
            omitted one is left unchanged. Everything else on a service — booking mode, stay rules,
            quantities, capacity — is read-only here.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | Service]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    *,
    client: AuthenticatedClient,
    body: ServiceUpdate,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> ErrorEnvelope | Service | None:
    """Update a service

     Update a service's name, description, price, duration or active state; omitted fields stay
    unchanged. Requires `services:write`. Limited to 120 requests per minute per account (API key) or
    per installation (OAuth).

    Args:
        service_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (ServiceUpdate): The service fields you can change. Every field is optional; an
            omitted one is left unchanged. Everything else on a service — booking mode, stay rules,
            quantities, capacity — is read-only here.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | Service
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
