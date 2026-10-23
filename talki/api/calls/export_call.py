from http import HTTPStatus
from io import BytesIO
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.export_format import ExportFormat
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    call_id: str,
    *,
    format_: ExportFormat | Unset = ExportFormat.PDF,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    params: dict[str, Any] = {}

    json_format_: str | Unset = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/calls/{call_id}/export".format(
            call_id=quote(str(call_id), safe=""),
        ),
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
    call_id: str,
    *,
    client: AuthenticatedClient,
    format_: ExportFormat | Unset = ExportFormat.PDF,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | File]:
    """Export a call

     Return one call as a PDF or Excel file, on every plan. It includes the conversation only with
    `transcripts:read` and when the account keeps transcripts, and the call's appointments only with
    `appointments:read`. Requires `calls:read`. Limited to 600 requests per minute per account (API key)
    or per installation (OAuth), and to 10 file exports per minute.

    Args:
        call_id (str):
        format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
            ExportFormat.PDF.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | File]
    """

    kwargs = _get_kwargs(
        call_id=call_id,
        format_=format_,
        talki_version=talki_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    call_id: str,
    *,
    client: AuthenticatedClient,
    format_: ExportFormat | Unset = ExportFormat.PDF,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | File | None:
    """Export a call

     Return one call as a PDF or Excel file, on every plan. It includes the conversation only with
    `transcripts:read` and when the account keeps transcripts, and the call's appointments only with
    `appointments:read`. Requires `calls:read`. Limited to 600 requests per minute per account (API key)
    or per installation (OAuth), and to 10 file exports per minute.

    Args:
        call_id (str):
        format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
            ExportFormat.PDF.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | File
    """

    return sync_detailed(
        call_id=call_id,
        client=client,
        format_=format_,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    call_id: str,
    *,
    client: AuthenticatedClient,
    format_: ExportFormat | Unset = ExportFormat.PDF,
    talki_version: str | Unset = UNSET,
) -> Response[ErrorEnvelope | File]:
    """Export a call

     Return one call as a PDF or Excel file, on every plan. It includes the conversation only with
    `transcripts:read` and when the account keeps transcripts, and the call's appointments only with
    `appointments:read`. Requires `calls:read`. Limited to 600 requests per minute per account (API key)
    or per installation (OAuth), and to 10 file exports per minute.

    Args:
        call_id (str):
        format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
            ExportFormat.PDF.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | File]
    """

    kwargs = _get_kwargs(
        call_id=call_id,
        format_=format_,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    call_id: str,
    *,
    client: AuthenticatedClient,
    format_: ExportFormat | Unset = ExportFormat.PDF,
    talki_version: str | Unset = UNSET,
) -> ErrorEnvelope | File | None:
    """Export a call

     Return one call as a PDF or Excel file, on every plan. It includes the conversation only with
    `transcripts:read` and when the account keeps transcripts, and the call's appointments only with
    `appointments:read`. Requires `calls:read`. Limited to 600 requests per minute per account (API key)
    or per installation (OAuth), and to 10 file exports per minute.

    Args:
        call_id (str):
        format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
            ExportFormat.PDF.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | File
    """

    return (
        await asyncio_detailed(
            call_id=call_id,
            client=client,
            format_=format_,
            talki_version=talki_version,
        )
    ).parsed
