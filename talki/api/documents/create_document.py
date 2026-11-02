from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document import Document
from ...models.document_create import DocumentCreate
from ...models.document_site_create import DocumentSiteCreate
from ...models.document_upload import DocumentUpload
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: DocumentCreate | DocumentSiteCreate | DocumentUpload | Unset = UNSET,
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
        "url": "/v1/documents",
        "params": params,
    }

    if isinstance(body, DocumentCreate | DocumentSiteCreate):
        if isinstance(body, DocumentCreate):
            _kwargs["json"] = body.to_dict()
        else:
            _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, DocumentUpload):
        _kwargs["files"] = body.to_multipart()

        headers["Content-Type"] = "multipart/form-data; boundary=+++"

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
) -> Document | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 202:
        response_202 = Document.from_dict(response.json())

        return response_202

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

    if response.status_code == 413:
        response_413 = ErrorEnvelope.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = ErrorEnvelope.from_dict(response.json())

        return response_415

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
) -> Response[Document | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: DocumentCreate | DocumentSiteCreate | DocumentUpload | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Document | ErrorEnvelope]:
    """Create a document

     Add a text note (`application/json`: `title`, `body`), import a website (`application/json`:
    `source: "website"`, `url`, optionally `pages`) or upload a file (`multipart/form-data`: `file`) to
    the knowledge base of the location `location_id` names, the main location's when omitted. A site
    already imported at one of the locations is refused (`conflict`): import it again with `PUT`.
    `location_ids` makes a copy at each of those locations too, sharing `copy_group_id`. Answers `202`
    with the document, `processing`: the assistant uses it once `document.updated` reports it `ready`,
    or `failed` with `status_error`. The plan's limits apply as in Talki: file size
    (`payload_too_large`), file type (`unsupported_file_type`), pages per site (`invalid_parameter`) and
    the account's knowledge storage (`payload_too_large`, or a site `failed` with `status_error`). A
    JSON field the note or the website does not take is refused (`invalid_parameter`). Requires
    `Idempotency-Key`. Requires `knowledge:write`. Limited to 120 requests per minute per account (API
    key) or per installation (OAuth), and to 60 document writes per minute, shared by creating,
    replacing and updating documents and discovering a site's pages.

    Args:
        location_id (None | str | Unset): The location the document is for, an id from `GET
            /v1/locations` (inactive ones included). Omit it for the main location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (DocumentCreate | DocumentSiteCreate):
        body (DocumentUpload): A file, sent as `multipart/form-data`: PDF, DOCX, XLSX, TXT or CSV,
            at most 10 MB or the plan's lower limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Document | ErrorEnvelope]
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
    body: DocumentCreate | DocumentSiteCreate | DocumentUpload | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Document | ErrorEnvelope | None:
    """Create a document

     Add a text note (`application/json`: `title`, `body`), import a website (`application/json`:
    `source: "website"`, `url`, optionally `pages`) or upload a file (`multipart/form-data`: `file`) to
    the knowledge base of the location `location_id` names, the main location's when omitted. A site
    already imported at one of the locations is refused (`conflict`): import it again with `PUT`.
    `location_ids` makes a copy at each of those locations too, sharing `copy_group_id`. Answers `202`
    with the document, `processing`: the assistant uses it once `document.updated` reports it `ready`,
    or `failed` with `status_error`. The plan's limits apply as in Talki: file size
    (`payload_too_large`), file type (`unsupported_file_type`), pages per site (`invalid_parameter`) and
    the account's knowledge storage (`payload_too_large`, or a site `failed` with `status_error`). A
    JSON field the note or the website does not take is refused (`invalid_parameter`). Requires
    `Idempotency-Key`. Requires `knowledge:write`. Limited to 120 requests per minute per account (API
    key) or per installation (OAuth), and to 60 document writes per minute, shared by creating,
    replacing and updating documents and discovering a site's pages.

    Args:
        location_id (None | str | Unset): The location the document is for, an id from `GET
            /v1/locations` (inactive ones included). Omit it for the main location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (DocumentCreate | DocumentSiteCreate):
        body (DocumentUpload): A file, sent as `multipart/form-data`: PDF, DOCX, XLSX, TXT or CSV,
            at most 10 MB or the plan's lower limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Document | ErrorEnvelope
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
    body: DocumentCreate | DocumentSiteCreate | DocumentUpload | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Document | ErrorEnvelope]:
    """Create a document

     Add a text note (`application/json`: `title`, `body`), import a website (`application/json`:
    `source: "website"`, `url`, optionally `pages`) or upload a file (`multipart/form-data`: `file`) to
    the knowledge base of the location `location_id` names, the main location's when omitted. A site
    already imported at one of the locations is refused (`conflict`): import it again with `PUT`.
    `location_ids` makes a copy at each of those locations too, sharing `copy_group_id`. Answers `202`
    with the document, `processing`: the assistant uses it once `document.updated` reports it `ready`,
    or `failed` with `status_error`. The plan's limits apply as in Talki: file size
    (`payload_too_large`), file type (`unsupported_file_type`), pages per site (`invalid_parameter`) and
    the account's knowledge storage (`payload_too_large`, or a site `failed` with `status_error`). A
    JSON field the note or the website does not take is refused (`invalid_parameter`). Requires
    `Idempotency-Key`. Requires `knowledge:write`. Limited to 120 requests per minute per account (API
    key) or per installation (OAuth), and to 60 document writes per minute, shared by creating,
    replacing and updating documents and discovering a site's pages.

    Args:
        location_id (None | str | Unset): The location the document is for, an id from `GET
            /v1/locations` (inactive ones included). Omit it for the main location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (DocumentCreate | DocumentSiteCreate):
        body (DocumentUpload): A file, sent as `multipart/form-data`: PDF, DOCX, XLSX, TXT or CSV,
            at most 10 MB or the plan's lower limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Document | ErrorEnvelope]
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
    body: DocumentCreate | DocumentSiteCreate | DocumentUpload | Unset = UNSET,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Document | ErrorEnvelope | None:
    """Create a document

     Add a text note (`application/json`: `title`, `body`), import a website (`application/json`:
    `source: "website"`, `url`, optionally `pages`) or upload a file (`multipart/form-data`: `file`) to
    the knowledge base of the location `location_id` names, the main location's when omitted. A site
    already imported at one of the locations is refused (`conflict`): import it again with `PUT`.
    `location_ids` makes a copy at each of those locations too, sharing `copy_group_id`. Answers `202`
    with the document, `processing`: the assistant uses it once `document.updated` reports it `ready`,
    or `failed` with `status_error`. The plan's limits apply as in Talki: file size
    (`payload_too_large`), file type (`unsupported_file_type`), pages per site (`invalid_parameter`) and
    the account's knowledge storage (`payload_too_large`, or a site `failed` with `status_error`). A
    JSON field the note or the website does not take is refused (`invalid_parameter`). Requires
    `Idempotency-Key`. Requires `knowledge:write`. Limited to 120 requests per minute per account (API
    key) or per installation (OAuth), and to 60 document writes per minute, shared by creating,
    replacing and updating documents and discovering a site's pages.

    Args:
        location_id (None | str | Unset): The location the document is for, an id from `GET
            /v1/locations` (inactive ones included). Omit it for the main location.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (DocumentCreate | DocumentSiteCreate):
        body (DocumentUpload): A file, sent as `multipart/form-data`: PDF, DOCX, XLSX, TXT or CSV,
            at most 10 MB or the plan's lower limit.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Document | ErrorEnvelope
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
