from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_test_message import AgentTestMessage
from ...models.agent_test_reply import AgentTestReply
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AgentTestMessage,
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
        "url": "/v1/agent_test",
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
) -> AgentTestReply | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = AgentTestReply.from_dict(response.json())

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

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AgentTestReply | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AgentTestMessage,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[AgentTestReply | ErrorEnvelope]:
    """Send a test message

     Send one message to the account's assistant, as a caller would say it, and return its answer: what a
    call to the location would hear, from the same settings, documents, services, calendar and partner
    tools, written as text. Nothing is saved: a booking the assistant makes is not made, and no call,
    appointment or unresolved request is recorded. The first message starts a session; send its
    `session_id` with the next ones. Talki keeps the history for 30 minutes after the last turn, and a
    session holds at most 20 turns (then `agent_test_session_full`). A session belongs to the credential
    that started it. Your app's own partner tools run, sent with `test_drive: true`, writes included; no
    other app's do. The assistant here runs on a text model, not the one that answers calls, so a reply
    can be worded differently from what a caller would hear. Refused while the managing partner has
    suspended the account (`account_suspended`). An account may send 25 test messages a day, shared with
    the test in the Talki apps, and an OAuth app 300 a day across all the accounts it is installed on;
    past either, `429` `rate_limit_exceeded` with `Retry-After`. Requires `account:write` and
    `knowledge:read`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth), and to 15 test messages per minute.

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (AgentTestMessage): One message to the assistant, as a caller would say it. Omit
            `session_id` to start a session, and send the one from the reply to continue it: Talki
            keeps the history, and there is no way to send one. A session stays at the location it
            started at.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentTestReply | ErrorEnvelope]
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
    body: AgentTestMessage,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> AgentTestReply | ErrorEnvelope | None:
    """Send a test message

     Send one message to the account's assistant, as a caller would say it, and return its answer: what a
    call to the location would hear, from the same settings, documents, services, calendar and partner
    tools, written as text. Nothing is saved: a booking the assistant makes is not made, and no call,
    appointment or unresolved request is recorded. The first message starts a session; send its
    `session_id` with the next ones. Talki keeps the history for 30 minutes after the last turn, and a
    session holds at most 20 turns (then `agent_test_session_full`). A session belongs to the credential
    that started it. Your app's own partner tools run, sent with `test_drive: true`, writes included; no
    other app's do. The assistant here runs on a text model, not the one that answers calls, so a reply
    can be worded differently from what a caller would hear. Refused while the managing partner has
    suspended the account (`account_suspended`). An account may send 25 test messages a day, shared with
    the test in the Talki apps, and an OAuth app 300 a day across all the accounts it is installed on;
    past either, `429` `rate_limit_exceeded` with `Retry-After`. Requires `account:write` and
    `knowledge:read`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth), and to 15 test messages per minute.

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (AgentTestMessage): One message to the assistant, as a caller would say it. Omit
            `session_id` to start a session, and send the one from the reply to continue it: Talki
            keeps the history, and there is no way to send one. A session stays at the location it
            started at.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentTestReply | ErrorEnvelope
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
    body: AgentTestMessage,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[AgentTestReply | ErrorEnvelope]:
    """Send a test message

     Send one message to the account's assistant, as a caller would say it, and return its answer: what a
    call to the location would hear, from the same settings, documents, services, calendar and partner
    tools, written as text. Nothing is saved: a booking the assistant makes is not made, and no call,
    appointment or unresolved request is recorded. The first message starts a session; send its
    `session_id` with the next ones. Talki keeps the history for 30 minutes after the last turn, and a
    session holds at most 20 turns (then `agent_test_session_full`). A session belongs to the credential
    that started it. Your app's own partner tools run, sent with `test_drive: true`, writes included; no
    other app's do. The assistant here runs on a text model, not the one that answers calls, so a reply
    can be worded differently from what a caller would hear. Refused while the managing partner has
    suspended the account (`account_suspended`). An account may send 25 test messages a day, shared with
    the test in the Talki apps, and an OAuth app 300 a day across all the accounts it is installed on;
    past either, `429` `rate_limit_exceeded` with `Retry-After`. Requires `account:write` and
    `knowledge:read`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth), and to 15 test messages per minute.

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (AgentTestMessage): One message to the assistant, as a caller would say it. Omit
            `session_id` to start a session, and send the one from the reply to continue it: Talki
            keeps the history, and there is no way to send one. A session stays at the location it
            started at.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentTestReply | ErrorEnvelope]
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
    body: AgentTestMessage,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> AgentTestReply | ErrorEnvelope | None:
    """Send a test message

     Send one message to the account's assistant, as a caller would say it, and return its answer: what a
    call to the location would hear, from the same settings, documents, services, calendar and partner
    tools, written as text. Nothing is saved: a booking the assistant makes is not made, and no call,
    appointment or unresolved request is recorded. The first message starts a session; send its
    `session_id` with the next ones. Talki keeps the history for 30 minutes after the last turn, and a
    session holds at most 20 turns (then `agent_test_session_full`). A session belongs to the credential
    that started it. Your app's own partner tools run, sent with `test_drive: true`, writes included; no
    other app's do. The assistant here runs on a text model, not the one that answers calls, so a reply
    can be worded differently from what a caller would hear. Refused while the managing partner has
    suspended the account (`account_suspended`). An account may send 25 test messages a day, shared with
    the test in the Talki apps, and an OAuth app 300 a day across all the accounts it is installed on;
    past either, `429` `rate_limit_exceeded` with `Retry-After`. Requires `account:write` and
    `knowledge:read`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth), and to 15 test messages per minute.

    Args:
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (AgentTestMessage): One message to the assistant, as a caller would say it. Omit
            `session_id` to start a session, and send the one from the reply to continue it: Talki
            keeps the history, and there is no way to send one. A session stays at the location it
            started at.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentTestReply | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
