from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.usage_history import UsageHistory
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    from_: None | str | Unset = UNSET,
    to: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    params: dict[str, Any] = {}

    json_from_: None | str | Unset
    if isinstance(from_, Unset):
        json_from_ = UNSET
    else:
        json_from_ = from_
    params["from"] = json_from_

    json_to: None | str | Unset
    if isinstance(to, Unset):
        json_to = UNSET
    else:
        json_to = to
    params["to"] = json_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/usage/history",
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
) -> ErrorEnvelope | UsageHistory | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = UsageHistory.from_dict(response.json())

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
) -> Response[ErrorEnvelope | UsageHistory]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    from_: None | str | Unset = UNSET,
    to: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | UsageHistory]:
    """Retrieve usage history

     Return the talk time billed in each calendar month, up to 13 months, oldest first. A call counts,
    whole, in the month it was answered in. Requires `account:read`. Limited to 600 requests per minute
    per account (API key) or per installation (OAuth).

    Args:
        from_ (None | str | Unset): First month, `YYYY-MM`. Default: 12 months before `to`.
        to (None | str | Unset): Last month, included, `YYYY-MM`. Default: the current month,
            which is still counting. Not after the current month. At most 13 months from `from`.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | UsageHistory]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
        talki_version=talki_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    from_: None | str | Unset = UNSET,
    to: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | UsageHistory | None:
    """Retrieve usage history

     Return the talk time billed in each calendar month, up to 13 months, oldest first. A call counts,
    whole, in the month it was answered in. Requires `account:read`. Limited to 600 requests per minute
    per account (API key) or per installation (OAuth).

    Args:
        from_ (None | str | Unset): First month, `YYYY-MM`. Default: 12 months before `to`.
        to (None | str | Unset): Last month, included, `YYYY-MM`. Default: the current month,
            which is still counting. Not after the current month. At most 13 months from `from`.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | UsageHistory
    """

    return sync_detailed(
        client=client,
        from_=from_,
        to=to,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    from_: None | str | Unset = UNSET,
    to: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | UsageHistory]:
    """Retrieve usage history

     Return the talk time billed in each calendar month, up to 13 months, oldest first. A call counts,
    whole, in the month it was answered in. Requires `account:read`. Limited to 600 requests per minute
    per account (API key) or per installation (OAuth).

    Args:
        from_ (None | str | Unset): First month, `YYYY-MM`. Default: 12 months before `to`.
        to (None | str | Unset): Last month, included, `YYYY-MM`. Default: the current month,
            which is still counting. Not after the current month. At most 13 months from `from`.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | UsageHistory]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    from_: None | str | Unset = UNSET,
    to: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | UsageHistory | None:
    """Retrieve usage history

     Return the talk time billed in each calendar month, up to 13 months, oldest first. A call counts,
    whole, in the month it was answered in. Requires `account:read`. Limited to 600 requests per minute
    per account (API key) or per installation (OAuth).

    Args:
        from_ (None | str | Unset): First month, `YYYY-MM`. Default: 12 months before `to`.
        to (None | str | Unset): Last month, included, `YYYY-MM`. Default: the current month,
            which is still counting. Not after the current month. At most 13 months from `from`.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | UsageHistory
    """

    return (
        await asyncio_detailed(
            client=client,
            from_=from_,
            to=to,
            talki_version=talki_version,
        )
    ).parsed
