from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.contact import Contact
from ...models.contact_upsert import ContactUpsert
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ContactUpsert,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/contacts",
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
) -> Contact | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = Contact.from_dict(response.json())

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
) -> Response[Contact | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ContactUpsert,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Contact | ErrorEnvelope]:
    """Upsert a contact

     Create or update a trusted contact by phone number or external reference. Requires `contacts:write`.
    Limited to 120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (ContactUpsert): Create or update the contact with this phone number: the number is
            the identity, and `external_id` is your cross-reference for finding it again after a
            number changes. A name written here is not overwritten by what the assistant hears on
            later calls. On a contact whose name was only guessed from a call, sending either name
            replaces both: the one you omit is cleared.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Contact | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        body=body,
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
    body: ContactUpsert,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Contact | ErrorEnvelope | None:
    """Upsert a contact

     Create or update a trusted contact by phone number or external reference. Requires `contacts:write`.
    Limited to 120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (ContactUpsert): Create or update the contact with this phone number: the number is
            the identity, and `external_id` is your cross-reference for finding it again after a
            number changes. A name written here is not overwritten by what the assistant hears on
            later calls. On a contact whose name was only guessed from a call, sending either name
            replaces both: the one you omit is cleared.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Contact | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ContactUpsert,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Contact | ErrorEnvelope]:
    """Upsert a contact

     Create or update a trusted contact by phone number or external reference. Requires `contacts:write`.
    Limited to 120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (ContactUpsert): Create or update the contact with this phone number: the number is
            the identity, and `external_id` is your cross-reference for finding it again after a
            number changes. A name written here is not overwritten by what the assistant hears on
            later calls. On a contact whose name was only guessed from a call, sending either name
            replaces both: the one you omit is cleared.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Contact | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ContactUpsert,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Contact | ErrorEnvelope | None:
    """Upsert a contact

     Create or update a trusted contact by phone number or external reference. Requires `contacts:write`.
    Limited to 120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (ContactUpsert): Create or update the contact with this phone number: the number is
            the identity, and `external_id` is your cross-reference for finding it again after a
            number changes. A name written here is not overwritten by what the assistant hears on
            later calls. On a contact whose name was only guessed from a call, sending either name
            replaces both: the one you omit is cleared.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Contact | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
