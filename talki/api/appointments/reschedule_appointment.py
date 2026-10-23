from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.appointment import Appointment
from ...models.appointment_reschedule import AppointmentReschedule
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    appointment_id: str,
    *,
    body: AppointmentReschedule,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/appointments/{appointment_id}".format(
            appointment_id=quote(str(appointment_id), safe=""),
        ),
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
) -> Appointment | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = Appointment.from_dict(response.json())

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
) -> Response[Appointment | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    appointment_id: str,
    *,
    client: AuthenticatedClient,
    body: AppointmentReschedule,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Appointment | ErrorEnvelope]:
    """Update an appointment

     Move or rename a booking while keeping its ID. A move is refused with `service_deleted` when a
    service of the booking has been deleted and the move would make that service's part of the booking
    end in the future, and with `location_inactive` when the booking's location is switched off; such a
    booking can still be renamed. Requires `Idempotency-Key`. Requires `appointments:write`. Limited to
    120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        appointment_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (AppointmentReschedule): A partial edit of a booking. Every field is optional, and an
            omitted field is left unchanged, not cleared. A move that does not fit is refused with a
            conflict code; nothing is booked. A booking never changes location.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Appointment | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        appointment_id=appointment_id,
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    appointment_id: str,
    *,
    client: AuthenticatedClient,
    body: AppointmentReschedule,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Appointment | ErrorEnvelope | None:
    """Update an appointment

     Move or rename a booking while keeping its ID. A move is refused with `service_deleted` when a
    service of the booking has been deleted and the move would make that service's part of the booking
    end in the future, and with `location_inactive` when the booking's location is switched off; such a
    booking can still be renamed. Requires `Idempotency-Key`. Requires `appointments:write`. Limited to
    120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        appointment_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (AppointmentReschedule): A partial edit of a booking. Every field is optional, and an
            omitted field is left unchanged, not cleared. A move that does not fit is refused with a
            conflict code; nothing is booked. A booking never changes location.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Appointment | ErrorEnvelope
    """

    return sync_detailed(
        appointment_id=appointment_id,
        client=client,
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    appointment_id: str,
    *,
    client: AuthenticatedClient,
    body: AppointmentReschedule,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Appointment | ErrorEnvelope]:
    """Update an appointment

     Move or rename a booking while keeping its ID. A move is refused with `service_deleted` when a
    service of the booking has been deleted and the move would make that service's part of the booking
    end in the future, and with `location_inactive` when the booking's location is switched off; such a
    booking can still be renamed. Requires `Idempotency-Key`. Requires `appointments:write`. Limited to
    120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        appointment_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (AppointmentReschedule): A partial edit of a booking. Every field is optional, and an
            omitted field is left unchanged, not cleared. A move that does not fit is refused with a
            conflict code; nothing is booked. A booking never changes location.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Appointment | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        appointment_id=appointment_id,
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    appointment_id: str,
    *,
    client: AuthenticatedClient,
    body: AppointmentReschedule,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Appointment | ErrorEnvelope | None:
    """Update an appointment

     Move or rename a booking while keeping its ID. A move is refused with `service_deleted` when a
    service of the booking has been deleted and the move would make that service's part of the booking
    end in the future, and with `location_inactive` when the booking's location is switched off; such a
    booking can still be renamed. Requires `Idempotency-Key`. Requires `appointments:write`. Limited to
    120 requests per minute per account (API key) or per installation (OAuth).

    Args:
        appointment_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (AppointmentReschedule): A partial edit of a booking. Every field is optional, and an
            omitted field is left unchanged, not cleared. A move that does not fit is refused with a
            conflict code; nothing is booked. A booking never changes location.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Appointment | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            appointment_id=appointment_id,
            client=client,
            body=body,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
