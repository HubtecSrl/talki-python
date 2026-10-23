from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.fake_call_request import FakeCallRequest
from ...models.fake_call_response import FakeCallResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: FakeCallRequest,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/sandbox/calls",
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
) -> ErrorEnvelope | FakeCallResponse | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 201:
        response_201 = FakeCallResponse.from_dict(response.json())

        return response_201

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
) -> Response[ErrorEnvelope | FakeCallResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: FakeCallRequest,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorEnvelope | FakeCallResponse]:
    """Create a sandbox call

     Tell the sandbox it had a call. The whole post-call flow runs for real, including signed webhook
    deliveries carrying `livemode: false`. Requires a developer sandbox; answers 404 on a real account.
    Limited to 30 requests per minute per account (API key) or per installation (OAuth).

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (FakeCallRequest): The call a sandbox should pretend it had.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | FakeCallResponse]
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
    body: FakeCallRequest,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> ErrorEnvelope | FakeCallResponse | None:
    """Create a sandbox call

     Tell the sandbox it had a call. The whole post-call flow runs for real, including signed webhook
    deliveries carrying `livemode: false`. Requires a developer sandbox; answers 404 on a real account.
    Limited to 30 requests per minute per account (API key) or per installation (OAuth).

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (FakeCallRequest): The call a sandbox should pretend it had.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | FakeCallResponse
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
    body: FakeCallRequest,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorEnvelope | FakeCallResponse]:
    """Create a sandbox call

     Tell the sandbox it had a call. The whole post-call flow runs for real, including signed webhook
    deliveries carrying `livemode: false`. Requires a developer sandbox; answers 404 on a real account.
    Limited to 30 requests per minute per account (API key) or per installation (OAuth).

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (FakeCallRequest): The call a sandbox should pretend it had.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | FakeCallResponse]
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
    body: FakeCallRequest,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> ErrorEnvelope | FakeCallResponse | None:
    """Create a sandbox call

     Tell the sandbox it had a call. The whole post-call flow runs for real, including signed webhook
    deliveries carrying `livemode: false`. Requires a developer sandbox; answers 404 on a real account.
    Limited to 30 requests per minute per account (API key) or per installation (OAuth).

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (FakeCallRequest): The call a sandbox should pretend it had.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | FakeCallResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
