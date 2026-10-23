from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.caller_rule import CallerRule
from ...models.caller_rule_create import CallerRuleCreate
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CallerRuleCreate,
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
        "url": "/v1/caller_rules",
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
) -> CallerRule | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = CallerRule.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = CallerRule.from_dict(response.json())

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
) -> Response[CallerRule | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CallerRuleCreate,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[CallerRule | ErrorEnvelope]:
    """Add a caller rule

     Add a number to the VIP or blocked list: `201` with the new rule. A number that already has a rule
    answers `200` with it, moved or relabelled as the request asks, or unchanged. Requires `Idempotency-
    Key`. Requires `contacts:write`. Limited to 120 requests per minute per account (API key) or per
    installation (OAuth), and to 20 creations per minute shared by the services, resources, tags and
    caller rules you create.

    Args:
        location_id (None | str | Unset): The location to add the number at, an id from `GET
            /v1/locations` (inactive ones included). Omit it for the main location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (CallerRuleCreate): A number to add. `201` creates a rule; `200` means the number
            already had one, which was moved or relabelled as the request asks, or returned unchanged.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallerRule | ErrorEnvelope]
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
    body: CallerRuleCreate,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> CallerRule | ErrorEnvelope | None:
    """Add a caller rule

     Add a number to the VIP or blocked list: `201` with the new rule. A number that already has a rule
    answers `200` with it, moved or relabelled as the request asks, or unchanged. Requires `Idempotency-
    Key`. Requires `contacts:write`. Limited to 120 requests per minute per account (API key) or per
    installation (OAuth), and to 20 creations per minute shared by the services, resources, tags and
    caller rules you create.

    Args:
        location_id (None | str | Unset): The location to add the number at, an id from `GET
            /v1/locations` (inactive ones included). Omit it for the main location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (CallerRuleCreate): A number to add. `201` creates a rule; `200` means the number
            already had one, which was moved or relabelled as the request asks, or returned unchanged.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallerRule | ErrorEnvelope
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
    body: CallerRuleCreate,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[CallerRule | ErrorEnvelope]:
    """Add a caller rule

     Add a number to the VIP or blocked list: `201` with the new rule. A number that already has a rule
    answers `200` with it, moved or relabelled as the request asks, or unchanged. Requires `Idempotency-
    Key`. Requires `contacts:write`. Limited to 120 requests per minute per account (API key) or per
    installation (OAuth), and to 20 creations per minute shared by the services, resources, tags and
    caller rules you create.

    Args:
        location_id (None | str | Unset): The location to add the number at, an id from `GET
            /v1/locations` (inactive ones included). Omit it for the main location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (CallerRuleCreate): A number to add. `201` creates a rule; `200` means the number
            already had one, which was moved or relabelled as the request asks, or returned unchanged.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallerRule | ErrorEnvelope]
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
    body: CallerRuleCreate,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> CallerRule | ErrorEnvelope | None:
    """Add a caller rule

     Add a number to the VIP or blocked list: `201` with the new rule. A number that already has a rule
    answers `200` with it, moved or relabelled as the request asks, or unchanged. Requires `Idempotency-
    Key`. Requires `contacts:write`. Limited to 120 requests per minute per account (API key) or per
    installation (OAuth), and to 20 creations per minute shared by the services, resources, tags and
    caller rules you create.

    Args:
        location_id (None | str | Unset): The location to add the number at, an id from `GET
            /v1/locations` (inactive ones included). Omit it for the main location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (CallerRuleCreate): A number to add. `201` creates a rule; `200` means the number
            already had one, which was moved or relabelled as the request asks, or returned unchanged.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallerRule | ErrorEnvelope
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
