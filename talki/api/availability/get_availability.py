import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.availability import Availability
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    service_id: str,
    from_: datetime.date,
    to: datetime.date,
    quantity: int | Unset = 1,
    stay_length: int | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    params: dict[str, Any] = {}

    params["service_id"] = service_id

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to = to.isoformat()
    params["to"] = json_to

    params["quantity"] = quantity

    json_stay_length: int | None | Unset
    if isinstance(stay_length, Unset):
        json_stay_length = UNSET
    else:
        json_stay_length = stay_length
    params["stay_length"] = json_stay_length

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/availability",
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
) -> Availability | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = Availability.from_dict(response.json())

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
) -> Response[Availability | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    service_id: str,
    from_: datetime.date,
    to: datetime.date,
    quantity: int | Unset = 1,
    stay_length: int | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[Availability | ErrorEnvelope]:
    """Retrieve availability

     Return advisory bookable windows for one service and local date range. Requires `availability:read`.
    Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        service_id (str): The service to check. Required. Availability is per service: two
            services that share a resource can return different windows.
        from_ (datetime.date): First local date to report, `YYYY-MM-DD`, in the account's
            timezone. Inclusive.
        to (datetime.date): Last local date to report, `YYYY-MM-DD`. Inclusive, so `from` equal to
            `to` asks about one day. At most 62 days per request.
        quantity (int | Unset): Party size, for a service that asks for one (`asks_quantity` on
            `GET /v1/services`). Pass the party size you intend to book: the windows depend on it.
            Ignored, and forced to 1, for a service that does not ask. Outside the service's
            `min_quantity`/`max_quantity` it is refused with 400 `invalid_parameter`, as the booking
            would be. Default: 1.
        stay_length (int | None | Unset): Length of the stay, in the service's `range_unit`
            (nights or days). **Required for a `day_range` service and rejected for any other.** Each
            date in the range then answers whether a stay of this length can begin on it.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Availability | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        from_=from_,
        to=to,
        quantity=quantity,
        stay_length=stay_length,
        talki_version=talki_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    service_id: str,
    from_: datetime.date,
    to: datetime.date,
    quantity: int | Unset = 1,
    stay_length: int | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Availability | ErrorEnvelope | None:
    """Retrieve availability

     Return advisory bookable windows for one service and local date range. Requires `availability:read`.
    Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        service_id (str): The service to check. Required. Availability is per service: two
            services that share a resource can return different windows.
        from_ (datetime.date): First local date to report, `YYYY-MM-DD`, in the account's
            timezone. Inclusive.
        to (datetime.date): Last local date to report, `YYYY-MM-DD`. Inclusive, so `from` equal to
            `to` asks about one day. At most 62 days per request.
        quantity (int | Unset): Party size, for a service that asks for one (`asks_quantity` on
            `GET /v1/services`). Pass the party size you intend to book: the windows depend on it.
            Ignored, and forced to 1, for a service that does not ask. Outside the service's
            `min_quantity`/`max_quantity` it is refused with 400 `invalid_parameter`, as the booking
            would be. Default: 1.
        stay_length (int | None | Unset): Length of the stay, in the service's `range_unit`
            (nights or days). **Required for a `day_range` service and rejected for any other.** Each
            date in the range then answers whether a stay of this length can begin on it.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Availability | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        service_id=service_id,
        from_=from_,
        to=to,
        quantity=quantity,
        stay_length=stay_length,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    service_id: str,
    from_: datetime.date,
    to: datetime.date,
    quantity: int | Unset = 1,
    stay_length: int | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[Availability | ErrorEnvelope]:
    """Retrieve availability

     Return advisory bookable windows for one service and local date range. Requires `availability:read`.
    Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        service_id (str): The service to check. Required. Availability is per service: two
            services that share a resource can return different windows.
        from_ (datetime.date): First local date to report, `YYYY-MM-DD`, in the account's
            timezone. Inclusive.
        to (datetime.date): Last local date to report, `YYYY-MM-DD`. Inclusive, so `from` equal to
            `to` asks about one day. At most 62 days per request.
        quantity (int | Unset): Party size, for a service that asks for one (`asks_quantity` on
            `GET /v1/services`). Pass the party size you intend to book: the windows depend on it.
            Ignored, and forced to 1, for a service that does not ask. Outside the service's
            `min_quantity`/`max_quantity` it is refused with 400 `invalid_parameter`, as the booking
            would be. Default: 1.
        stay_length (int | None | Unset): Length of the stay, in the service's `range_unit`
            (nights or days). **Required for a `day_range` service and rejected for any other.** Each
            date in the range then answers whether a stay of this length can begin on it.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Availability | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        from_=from_,
        to=to,
        quantity=quantity,
        stay_length=stay_length,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    service_id: str,
    from_: datetime.date,
    to: datetime.date,
    quantity: int | Unset = 1,
    stay_length: int | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Availability | ErrorEnvelope | None:
    """Retrieve availability

     Return advisory bookable windows for one service and local date range. Requires `availability:read`.
    Limited to 600 requests per minute per account (API key) or per installation (OAuth).

    Args:
        service_id (str): The service to check. Required. Availability is per service: two
            services that share a resource can return different windows.
        from_ (datetime.date): First local date to report, `YYYY-MM-DD`, in the account's
            timezone. Inclusive.
        to (datetime.date): Last local date to report, `YYYY-MM-DD`. Inclusive, so `from` equal to
            `to` asks about one day. At most 62 days per request.
        quantity (int | Unset): Party size, for a service that asks for one (`asks_quantity` on
            `GET /v1/services`). Pass the party size you intend to book: the windows depend on it.
            Ignored, and forced to 1, for a service that does not ask. Outside the service's
            `min_quantity`/`max_quantity` it is refused with 400 `invalid_parameter`, as the booking
            would be. Default: 1.
        stay_length (int | None | Unset): Length of the stay, in the service's `range_unit`
            (nights or days). **Required for a `day_range` service and rejected for any other.** Each
            date in the range then answers whether a stay of this length can begin on it.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Availability | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            service_id=service_id,
            from_=from_,
            to=to,
            quantity=quantity,
            stay_length=stay_length,
            talki_version=talki_version,
        )
    ).parsed
