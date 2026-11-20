from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.whats_app_conversation_list import WhatsAppConversationList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    needs_answer: bool | Unset = False,
    limit: int | Unset = 30,
    cursor: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    params: dict[str, Any] = {}

    params["needs_answer"] = needs_answer

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
        "url": "/v1/whatsapp/conversations",
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
) -> ErrorEnvelope | WhatsAppConversationList | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = WhatsAppConversationList.from_dict(response.json())

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
) -> Response[ErrorEnvelope | WhatsAppConversationList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    needs_answer: bool | Unset = False,
    limit: int | Unset = 30,
    cursor: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | WhatsAppConversationList]:
    """List WhatsApp conversations

     Return the conversations Talki took part in or kept out of, newest first. `needs_answer=true` lists
    those waiting for the owner's «è un cliente?». Requires `whatsapp:read`. Limited to 600 requests per
    minute per account (API key) or per installation (OAuth).

    Args:
        needs_answer (bool | Unset): Only the conversations whose «è un cliente?» waits for the
            owner's answer. Default: False.
        limit (int | Unset): Maximum number of conversations to return. Default: 30.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | WhatsAppConversationList]
    """

    kwargs = _get_kwargs(
        needs_answer=needs_answer,
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
    needs_answer: bool | Unset = False,
    limit: int | Unset = 30,
    cursor: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | WhatsAppConversationList | None:
    """List WhatsApp conversations

     Return the conversations Talki took part in or kept out of, newest first. `needs_answer=true` lists
    those waiting for the owner's «è un cliente?». Requires `whatsapp:read`. Limited to 600 requests per
    minute per account (API key) or per installation (OAuth).

    Args:
        needs_answer (bool | Unset): Only the conversations whose «è un cliente?» waits for the
            owner's answer. Default: False.
        limit (int | Unset): Maximum number of conversations to return. Default: 30.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | WhatsAppConversationList
    """

    return sync_detailed(
        client=client,
        needs_answer=needs_answer,
        limit=limit,
        cursor=cursor,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    needs_answer: bool | Unset = False,
    limit: int | Unset = 30,
    cursor: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | WhatsAppConversationList]:
    """List WhatsApp conversations

     Return the conversations Talki took part in or kept out of, newest first. `needs_answer=true` lists
    those waiting for the owner's «è un cliente?». Requires `whatsapp:read`. Limited to 600 requests per
    minute per account (API key) or per installation (OAuth).

    Args:
        needs_answer (bool | Unset): Only the conversations whose «è un cliente?» waits for the
            owner's answer. Default: False.
        limit (int | Unset): Maximum number of conversations to return. Default: 30.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | WhatsAppConversationList]
    """

    kwargs = _get_kwargs(
        needs_answer=needs_answer,
        limit=limit,
        cursor=cursor,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    needs_answer: bool | Unset = False,
    limit: int | Unset = 30,
    cursor: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | WhatsAppConversationList | None:
    """List WhatsApp conversations

     Return the conversations Talki took part in or kept out of, newest first. `needs_answer=true` lists
    those waiting for the owner's «è un cliente?». Requires `whatsapp:read`. Limited to 600 requests per
    minute per account (API key) or per installation (OAuth).

    Args:
        needs_answer (bool | Unset): Only the conversations whose «è un cliente?» waits for the
            owner's answer. Default: False.
        limit (int | Unset): Maximum number of conversations to return. Default: 30.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | WhatsAppConversationList
    """

    return (
        await asyncio_detailed(
            client=client,
            needs_answer=needs_answer,
            limit=limit,
            cursor=cursor,
            talki_version=talki_version,
        )
    ).parsed
