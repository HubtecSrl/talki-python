from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_tools import AgentTools
from ...models.agent_tools_update import AgentToolsUpdate
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AgentToolsUpdate,
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
        "method": "patch",
        "url": "/v1/agent_tools",
        "params": params,
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
) -> AgentTools | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = AgentTools.from_dict(response.json())

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
) -> Response[AgentTools | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AgentToolsUpdate,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[AgentTools | ErrorEnvelope]:
    """Update the agent tools

     Replace the list of tools the assistant may call: the account's, or with `location_id` that
    location's own, which replaces the account's there. Only tools with an approved revision can be
    switched on, and `[]` switches every tool off. `"enabled": null` with `location_id` drops the
    location's own list, so it follows the account's again; the account's list cannot be null. One call
    has at most `limit_per_call` agent tools, counted across every app the account granted
    `agent_tools:write`, those the owner switched off included: a change that raises any location's
    count above that is refused (`tool_limit`), and one that does not raise it never is. While the owner
    has switched your app's tools off (`owner_off`), the lists are kept and none of the tools reaches a
    call. Only your app's OAuth access token is accepted, as for `GET`; an API key is refused
    (`insufficient_scope`). Requires `agent_tools:write`. Limited to 120 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        location_id (None | str | Unset): A location's own list, an id from `GET /v1/locations`.
            Omit it for the account's list, used at every location without its own.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (AgentToolsUpdate): The list of tools to switch on, replacing the one stored at this
            level.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentTools | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        body=body,
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
    body: AgentToolsUpdate,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> AgentTools | ErrorEnvelope | None:
    """Update the agent tools

     Replace the list of tools the assistant may call: the account's, or with `location_id` that
    location's own, which replaces the account's there. Only tools with an approved revision can be
    switched on, and `[]` switches every tool off. `"enabled": null` with `location_id` drops the
    location's own list, so it follows the account's again; the account's list cannot be null. One call
    has at most `limit_per_call` agent tools, counted across every app the account granted
    `agent_tools:write`, those the owner switched off included: a change that raises any location's
    count above that is refused (`tool_limit`), and one that does not raise it never is. While the owner
    has switched your app's tools off (`owner_off`), the lists are kept and none of the tools reaches a
    call. Only your app's OAuth access token is accepted, as for `GET`; an API key is refused
    (`insufficient_scope`). Requires `agent_tools:write`. Limited to 120 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        location_id (None | str | Unset): A location's own list, an id from `GET /v1/locations`.
            Omit it for the account's list, used at every location without its own.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (AgentToolsUpdate): The list of tools to switch on, replacing the one stored at this
            level.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentTools | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        body=body,
        location_id=location_id,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AgentToolsUpdate,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[AgentTools | ErrorEnvelope]:
    """Update the agent tools

     Replace the list of tools the assistant may call: the account's, or with `location_id` that
    location's own, which replaces the account's there. Only tools with an approved revision can be
    switched on, and `[]` switches every tool off. `"enabled": null` with `location_id` drops the
    location's own list, so it follows the account's again; the account's list cannot be null. One call
    has at most `limit_per_call` agent tools, counted across every app the account granted
    `agent_tools:write`, those the owner switched off included: a change that raises any location's
    count above that is refused (`tool_limit`), and one that does not raise it never is. While the owner
    has switched your app's tools off (`owner_off`), the lists are kept and none of the tools reaches a
    call. Only your app's OAuth access token is accepted, as for `GET`; an API key is refused
    (`insufficient_scope`). Requires `agent_tools:write`. Limited to 120 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        location_id (None | str | Unset): A location's own list, an id from `GET /v1/locations`.
            Omit it for the account's list, used at every location without its own.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (AgentToolsUpdate): The list of tools to switch on, replacing the one stored at this
            level.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentTools | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        body=body,
        location_id=location_id,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AgentToolsUpdate,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> AgentTools | ErrorEnvelope | None:
    """Update the agent tools

     Replace the list of tools the assistant may call: the account's, or with `location_id` that
    location's own, which replaces the account's there. Only tools with an approved revision can be
    switched on, and `[]` switches every tool off. `"enabled": null` with `location_id` drops the
    location's own list, so it follows the account's again; the account's list cannot be null. One call
    has at most `limit_per_call` agent tools, counted across every app the account granted
    `agent_tools:write`, those the owner switched off included: a change that raises any location's
    count above that is refused (`tool_limit`), and one that does not raise it never is. While the owner
    has switched your app's tools off (`owner_off`), the lists are kept and none of the tools reaches a
    call. Only your app's OAuth access token is accepted, as for `GET`; an API key is refused
    (`insufficient_scope`). Requires `agent_tools:write`. Limited to 120 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        location_id (None | str | Unset): A location's own list, an id from `GET /v1/locations`.
            Omit it for the account's list, used at every location without its own.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (AgentToolsUpdate): The list of tools to switch on, replacing the one stored at this
            level.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentTools | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            location_id=location_id,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
