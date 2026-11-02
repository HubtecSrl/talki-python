from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document_list import DocumentList
from ...models.error_envelope import ErrorEnvelope
from ...models.list_documents_source_type_0 import ListDocumentsSourceType0
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    source: ListDocumentsSourceType0 | None | Unset = UNSET,
    enabled: bool | None | Unset = UNSET,
    faq: bool | None | Unset = UNSET,
    copy_group_id: None | str | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    params: dict[str, Any] = {}

    params["limit"] = limit

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    json_source: None | str | Unset
    if isinstance(source, Unset):
        json_source = UNSET
    elif isinstance(source, ListDocumentsSourceType0):
        json_source = source.value
    else:
        json_source = source
    params["source"] = json_source

    json_enabled: bool | None | Unset
    if isinstance(enabled, Unset):
        json_enabled = UNSET
    else:
        json_enabled = enabled
    params["enabled"] = json_enabled

    json_faq: bool | None | Unset
    if isinstance(faq, Unset):
        json_faq = UNSET
    else:
        json_faq = faq
    params["faq"] = json_faq

    json_copy_group_id: None | str | Unset
    if isinstance(copy_group_id, Unset):
        json_copy_group_id = UNSET
    else:
        json_copy_group_id = copy_group_id
    params["copy_group_id"] = json_copy_group_id

    json_location_id: None | str | Unset
    if isinstance(location_id, Unset):
        json_location_id = UNSET
    else:
        json_location_id = location_id
    params["location_id"] = json_location_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/documents",
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
) -> DocumentList | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = DocumentList.from_dict(response.json())

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
) -> Response[DocumentList | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    source: ListDocumentsSourceType0 | None | Unset = UNSET,
    enabled: bool | None | Unset = UNSET,
    faq: bool | None | Unset = UNSET,
    copy_group_id: None | str | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[DocumentList | ErrorEnvelope]:
    """List documents

     Return the knowledge-base documents of every location, or of one, newest first, whatever their
    `status`: an upload is listed from the moment it is received. `document.*` events report every
    change, `status` included. Requires `knowledge:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of documents to return. Default: 50.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page.
        source (ListDocumentsSourceType0 | None | Unset): Only `text` notes, uploaded `file`s or
            imported `website`s.
        enabled (bool | None | Unset): Only documents switched on (`true`) or off (`false`).
        faq (bool | None | Unset): Only the locations' FAQ notes (`true`), or every other document
            (`false`).
        copy_group_id (None | str | Unset): Only the copies sharing this `copy_group_id`.
        location_id (None | str | Unset): Only the records of this location, an id from `GET
            /v1/locations` (inactive ones included). Omit for every location: each record carries its
            `location_id`.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentList | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        source=source,
        enabled=enabled,
        faq=faq,
        copy_group_id=copy_group_id,
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
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    source: ListDocumentsSourceType0 | None | Unset = UNSET,
    enabled: bool | None | Unset = UNSET,
    faq: bool | None | Unset = UNSET,
    copy_group_id: None | str | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> DocumentList | ErrorEnvelope | None:
    """List documents

     Return the knowledge-base documents of every location, or of one, newest first, whatever their
    `status`: an upload is listed from the moment it is received. `document.*` events report every
    change, `status` included. Requires `knowledge:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of documents to return. Default: 50.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page.
        source (ListDocumentsSourceType0 | None | Unset): Only `text` notes, uploaded `file`s or
            imported `website`s.
        enabled (bool | None | Unset): Only documents switched on (`true`) or off (`false`).
        faq (bool | None | Unset): Only the locations' FAQ notes (`true`), or every other document
            (`false`).
        copy_group_id (None | str | Unset): Only the copies sharing this `copy_group_id`.
        location_id (None | str | Unset): Only the records of this location, an id from `GET
            /v1/locations` (inactive ones included). Omit for every location: each record carries its
            `location_id`.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DocumentList | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        source=source,
        enabled=enabled,
        faq=faq,
        copy_group_id=copy_group_id,
        location_id=location_id,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    source: ListDocumentsSourceType0 | None | Unset = UNSET,
    enabled: bool | None | Unset = UNSET,
    faq: bool | None | Unset = UNSET,
    copy_group_id: None | str | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[DocumentList | ErrorEnvelope]:
    """List documents

     Return the knowledge-base documents of every location, or of one, newest first, whatever their
    `status`: an upload is listed from the moment it is received. `document.*` events report every
    change, `status` included. Requires `knowledge:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of documents to return. Default: 50.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page.
        source (ListDocumentsSourceType0 | None | Unset): Only `text` notes, uploaded `file`s or
            imported `website`s.
        enabled (bool | None | Unset): Only documents switched on (`true`) or off (`false`).
        faq (bool | None | Unset): Only the locations' FAQ notes (`true`), or every other document
            (`false`).
        copy_group_id (None | str | Unset): Only the copies sharing this `copy_group_id`.
        location_id (None | str | Unset): Only the records of this location, an id from `GET
            /v1/locations` (inactive ones included). Omit for every location: each record carries its
            `location_id`.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentList | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        source=source,
        enabled=enabled,
        faq=faq,
        copy_group_id=copy_group_id,
        location_id=location_id,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    source: ListDocumentsSourceType0 | None | Unset = UNSET,
    enabled: bool | None | Unset = UNSET,
    faq: bool | None | Unset = UNSET,
    copy_group_id: None | str | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> DocumentList | ErrorEnvelope | None:
    """List documents

     Return the knowledge-base documents of every location, or of one, newest first, whatever their
    `status`: an upload is listed from the moment it is received. `document.*` events report every
    change, `status` included. Requires `knowledge:read`. Limited to 600 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        limit (int | Unset): Maximum number of documents to return. Default: 50.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
            for the first page.
        source (ListDocumentsSourceType0 | None | Unset): Only `text` notes, uploaded `file`s or
            imported `website`s.
        enabled (bool | None | Unset): Only documents switched on (`true`) or off (`false`).
        faq (bool | None | Unset): Only the locations' FAQ notes (`true`), or every other document
            (`false`).
        copy_group_id (None | str | Unset): Only the copies sharing this `copy_group_id`.
        location_id (None | str | Unset): Only the records of this location, an id from `GET
            /v1/locations` (inactive ones included). Omit for every location: each record carries its
            `location_id`.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DocumentList | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            source=source,
            enabled=enabled,
            faq=faq,
            copy_group_id=copy_group_id,
            location_id=location_id,
            talki_version=talki_version,
        )
    ).parsed
