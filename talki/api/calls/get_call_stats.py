import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_stats import CallStats
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    days: int | None | Unset = UNSET,
    from_: datetime.date | None | Unset = UNSET,
    to: datetime.date | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    params: dict[str, Any] = {}

    json_days: int | None | Unset
    if isinstance(days, Unset):
        json_days = UNSET
    else:
        json_days = days
    params["days"] = json_days

    json_from_: None | str | Unset
    if isinstance(from_, Unset):
        json_from_ = UNSET
    elif isinstance(from_, datetime.date):
        json_from_ = from_.isoformat()
    else:
        json_from_ = from_
    params["from"] = json_from_

    json_to: None | str | Unset
    if isinstance(to, Unset):
        json_to = UNSET
    elif isinstance(to, datetime.date):
        json_to = to.isoformat()
    else:
        json_to = to
    params["to"] = json_to

    json_location_id: None | str | Unset
    if isinstance(location_id, Unset):
        json_location_id = UNSET
    else:
        json_location_id = location_id
    params["location_id"] = json_location_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/calls/stats",
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
) -> CallStats | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = CallStats.from_dict(response.json())

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
) -> Response[CallStats | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    days: int | None | Unset = UNSET,
    from_: datetime.date | None | Unset = UNSET,
    to: datetime.date | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[CallStats | ErrorEnvelope]:
    """Retrieve call statistics

     Return totals, the daily series and the top callers over the last `days`, or over the local days
    `from` to `to` (at most 366). Requires `calls:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        days (int | None | Unset): Length of the period, in days, ending now. Default 30. Cannot
            be combined with `from` / `to`.
        from_ (datetime.date | None | Unset): First day of the period, `YYYY-MM-DD`, local to the
            account's `timezone`. Sent with `to`, instead of `days`.
        to (datetime.date | None | Unset): Last day of the period, included, `YYYY-MM-DD`. At most
            366 days after `from`.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallStats | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        days=days,
        from_=from_,
        to=to,
        location_id=location_id,
        talki_version=talki_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    days: int | None | Unset = UNSET,
    from_: datetime.date | None | Unset = UNSET,
    to: datetime.date | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> CallStats | ErrorEnvelope | None:
    """Retrieve call statistics

     Return totals, the daily series and the top callers over the last `days`, or over the local days
    `from` to `to` (at most 366). Requires `calls:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        days (int | None | Unset): Length of the period, in days, ending now. Default 30. Cannot
            be combined with `from` / `to`.
        from_ (datetime.date | None | Unset): First day of the period, `YYYY-MM-DD`, local to the
            account's `timezone`. Sent with `to`, instead of `days`.
        to (datetime.date | None | Unset): Last day of the period, included, `YYYY-MM-DD`. At most
            366 days after `from`.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallStats | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        days=days,
        from_=from_,
        to=to,
        location_id=location_id,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    days: int | None | Unset = UNSET,
    from_: datetime.date | None | Unset = UNSET,
    to: datetime.date | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[CallStats | ErrorEnvelope]:
    """Retrieve call statistics

     Return totals, the daily series and the top callers over the last `days`, or over the local days
    `from` to `to` (at most 366). Requires `calls:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        days (int | None | Unset): Length of the period, in days, ending now. Default 30. Cannot
            be combined with `from` / `to`.
        from_ (datetime.date | None | Unset): First day of the period, `YYYY-MM-DD`, local to the
            account's `timezone`. Sent with `to`, instead of `days`.
        to (datetime.date | None | Unset): Last day of the period, included, `YYYY-MM-DD`. At most
            366 days after `from`.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallStats | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        days=days,
        from_=from_,
        to=to,
        location_id=location_id,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    days: int | None | Unset = UNSET,
    from_: datetime.date | None | Unset = UNSET,
    to: datetime.date | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> CallStats | ErrorEnvelope | None:
    """Retrieve call statistics

     Return totals, the daily series and the top callers over the last `days`, or over the local days
    `from` to `to` (at most 366). Requires `calls:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        days (int | None | Unset): Length of the period, in days, ending now. Default 30. Cannot
            be combined with `from` / `to`.
        from_ (datetime.date | None | Unset): First day of the period, `YYYY-MM-DD`, local to the
            account's `timezone`. Sent with `to`, instead of `days`.
        to (datetime.date | None | Unset): Last day of the period, included, `YYYY-MM-DD`. At most
            366 days after `from`.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallStats | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            days=days,
            from_=from_,
            to=to,
            location_id=location_id,
            talki_version=talki_version,
        )
    ).parsed
