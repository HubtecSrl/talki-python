from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.whats_app_conversation_messages import WhatsAppConversationMessages
from ...types import UNSET, Response, Unset


def _get_kwargs(
    conversation_id: str,
    *,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/whatsapp/conversations/{conversation_id}/messages".format(
            conversation_id=quote(str(conversation_id), safe=""),
        ),
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
) -> ErrorEnvelope | WhatsAppConversationMessages | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = WhatsAppConversationMessages.from_dict(response.json())

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
) -> Response[ErrorEnvelope | WhatsAppConversationMessages]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | WhatsAppConversationMessages]:
    """Retrieve a WhatsApp conversation's messages

     Return the messages of one conversation, oldest first. `whatsapp:read` does not grant them: the
    account owner ticks `transcripts:read` on its own. Messages are kept 30 days. Requires
    `transcripts:read`. Limited to 600 requests per minute per account (API key) or per installation
    (OAuth).

    Args:
        conversation_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | WhatsAppConversationMessages]
    """

    kwargs = _get_kwargs(
        conversation_id=conversation_id,
        talki_version=talki_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | WhatsAppConversationMessages | None:
    """Retrieve a WhatsApp conversation's messages

     Return the messages of one conversation, oldest first. `whatsapp:read` does not grant them: the
    account owner ticks `transcripts:read` on its own. Messages are kept 30 days. Requires
    `transcripts:read`. Limited to 600 requests per minute per account (API key) or per installation
    (OAuth).

    Args:
        conversation_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | WhatsAppConversationMessages
    """

    return sync_detailed(
        conversation_id=conversation_id,
        client=client,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | WhatsAppConversationMessages]:
    """Retrieve a WhatsApp conversation's messages

     Return the messages of one conversation, oldest first. `whatsapp:read` does not grant them: the
    account owner ticks `transcripts:read` on its own. Messages are kept 30 days. Requires
    `transcripts:read`. Limited to 600 requests per minute per account (API key) or per installation
    (OAuth).

    Args:
        conversation_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | WhatsAppConversationMessages]
    """

    kwargs = _get_kwargs(
        conversation_id=conversation_id,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    conversation_id: str,
    *,
    client: AuthenticatedClient,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | WhatsAppConversationMessages | None:
    """Retrieve a WhatsApp conversation's messages

     Return the messages of one conversation, oldest first. `whatsapp:read` does not grant them: the
    account owner ticks `transcripts:read` on its own. Messages are kept 30 days. Requires
    `transcripts:read`. Limited to 600 requests per minute per account (API key) or per installation
    (OAuth).

    Args:
        conversation_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | WhatsAppConversationMessages
    """

    return (
        await asyncio_detailed(
            conversation_id=conversation_id,
            client=client,
            talki_version=talki_version,
        )
    ).parsed
