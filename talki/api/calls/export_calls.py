import datetime
from http import HTTPStatus
from io import BytesIO
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_outcome import CallOutcome
from ...models.error_envelope import ErrorEnvelope
from ...models.export_format import ExportFormat
from ...models.inbox_status import InboxStatus
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    *,
    from_: datetime.date,
    to: datetime.date,
    format_: ExportFormat | Unset = ExportFormat.PDF,
    status: InboxStatus | Unset = InboxStatus.ALL,
    q: None | str | Unset = UNSET,
    outcome: CallOutcome | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    params: dict[str, Any] = {}

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to = to.isoformat()
    params["to"] = json_to

    json_format_: str | Unset = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    json_q: None | str | Unset
    if isinstance(q, Unset):
        json_q = UNSET
    else:
        json_q = q
    params["q"] = json_q

    json_outcome: None | str | Unset
    if isinstance(outcome, Unset):
        json_outcome = UNSET
    elif isinstance(outcome, CallOutcome):
        json_outcome = outcome.value
    else:
        json_outcome = outcome
    params["outcome"] = json_outcome

    json_location_id: None | str | Unset
    if isinstance(location_id, Unset):
        json_location_id = UNSET
    else:
        json_location_id = location_id
    params["location_id"] = json_location_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/calls/export",
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


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorEnvelope | File | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

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
) -> Response[ErrorEnvelope | File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    from_: datetime.date,
    to: datetime.date,
    format_: ExportFormat | Unset = ExportFormat.PDF,
    status: InboxStatus | Unset = InboxStatus.ALL,
    q: None | str | Unset = UNSET,
    outcome: CallOutcome | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | File]:
    """Export the call log

     Return the calls of a date range as a PDF or Excel file, without transcripts. `status` defaults to
    `all`; `status`, `q` and `outcome` narrow the file as they narrow `GET /v1/calls`. Each call's
    appointments are included only when the credential also holds `appointments:read`. Needs a plan that
    includes the call log export. Requires `calls:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth), and to 10 file exports per minute.

    Args:
        from_ (datetime.date): First day, `YYYY-MM-DD`, local to the account's `timezone`.
        to (datetime.date): Last day, included, `YYYY-MM-DD`. At most 366 days after `from`.
        format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
            ExportFormat.PDF.
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
            contains it, or whose caller's `display_name` does. A name that is not published as
            `display_name` is not searched either.
        outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
            `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
            outcomes were tracked have none and match no value.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | File]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
        format_=format_,
        status=status,
        q=q,
        outcome=outcome,
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
    from_: datetime.date,
    to: datetime.date,
    format_: ExportFormat | Unset = ExportFormat.PDF,
    status: InboxStatus | Unset = InboxStatus.ALL,
    q: None | str | Unset = UNSET,
    outcome: CallOutcome | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | File | None:
    """Export the call log

     Return the calls of a date range as a PDF or Excel file, without transcripts. `status` defaults to
    `all`; `status`, `q` and `outcome` narrow the file as they narrow `GET /v1/calls`. Each call's
    appointments are included only when the credential also holds `appointments:read`. Needs a plan that
    includes the call log export. Requires `calls:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth), and to 10 file exports per minute.

    Args:
        from_ (datetime.date): First day, `YYYY-MM-DD`, local to the account's `timezone`.
        to (datetime.date): Last day, included, `YYYY-MM-DD`. At most 366 days after `from`.
        format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
            ExportFormat.PDF.
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
            contains it, or whose caller's `display_name` does. A name that is not published as
            `display_name` is not searched either.
        outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
            `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
            outcomes were tracked have none and match no value.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | File
    """

    return sync_detailed(
        client=client,
        from_=from_,
        to=to,
        format_=format_,
        status=status,
        q=q,
        outcome=outcome,
        location_id=location_id,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    from_: datetime.date,
    to: datetime.date,
    format_: ExportFormat | Unset = ExportFormat.PDF,
    status: InboxStatus | Unset = InboxStatus.ALL,
    q: None | str | Unset = UNSET,
    outcome: CallOutcome | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | File]:
    """Export the call log

     Return the calls of a date range as a PDF or Excel file, without transcripts. `status` defaults to
    `all`; `status`, `q` and `outcome` narrow the file as they narrow `GET /v1/calls`. Each call's
    appointments are included only when the credential also holds `appointments:read`. Needs a plan that
    includes the call log export. Requires `calls:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth), and to 10 file exports per minute.

    Args:
        from_ (datetime.date): First day, `YYYY-MM-DD`, local to the account's `timezone`.
        to (datetime.date): Last day, included, `YYYY-MM-DD`. At most 366 days after `from`.
        format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
            ExportFormat.PDF.
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
            contains it, or whose caller's `display_name` does. A name that is not published as
            `display_name` is not searched either.
        outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
            `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
            outcomes were tracked have none and match no value.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | File]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
        format_=format_,
        status=status,
        q=q,
        outcome=outcome,
        location_id=location_id,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    from_: datetime.date,
    to: datetime.date,
    format_: ExportFormat | Unset = ExportFormat.PDF,
    status: InboxStatus | Unset = InboxStatus.ALL,
    q: None | str | Unset = UNSET,
    outcome: CallOutcome | None | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | File | None:
    """Export the call log

     Return the calls of a date range as a PDF or Excel file, without transcripts. `status` defaults to
    `all`; `status`, `q` and `outcome` narrow the file as they narrow `GET /v1/calls`. Each call's
    appointments are included only when the credential also holds `appointments:read`. Needs a plan that
    includes the call log export. Requires `calls:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth), and to 10 file exports per minute.

    Args:
        from_ (datetime.date): First day, `YYYY-MM-DD`, local to the account's `timezone`.
        to (datetime.date): Last day, included, `YYYY-MM-DD`. At most 366 days after `from`.
        format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
            ExportFormat.PDF.
        status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
            and not yet read. `archived` — archived calls. `all` — every call. Default:
            InboxStatus.ALL.
        q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
            contains it, or whose caller's `display_name` does. A name that is not published as
            `display_name` is not searched either.
        outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
            `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
            outcomes were tracked have none and match no value.
        location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
            id from `GET /v1/locations`. Omit for every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | File
    """

    return (
        await asyncio_detailed(
            client=client,
            from_=from_,
            to=to,
            format_=format_,
            status=status,
            q=q,
            outcome=outcome,
            location_id=location_id,
            talki_version=talki_version,
        )
    ).parsed
