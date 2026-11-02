from http import HTTPStatus
from typing import Any, Literal
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document import Document
from ...models.document_file_replace import DocumentFileReplace
from ...models.document_replace import DocumentReplace
from ...models.document_site_replace import DocumentSiteReplace
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    document_id: str,
    *,
    body: DocumentReplace | DocumentSiteReplace | DocumentFileReplace | Unset = UNSET,
    also: Literal["copies"] | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    params: dict[str, Any] = {}

    json_also: Literal["copies"] | None | Unset
    if isinstance(also, Unset):
        json_also = UNSET
    else:
        json_also = also
    params["also"] = json_also

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/documents/{document_id}".format(
            document_id=quote(str(document_id), safe=""),
        ),
        "params": params,
    }

    if isinstance(body, DocumentReplace | DocumentSiteReplace):
        if isinstance(body, DocumentReplace):
            _kwargs["json"] = body.to_dict()
        else:
            _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, DocumentFileReplace):
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
    document_id: str,
    *,
    client: AuthenticatedClient,
    body: DocumentReplace | DocumentSiteReplace | DocumentFileReplace | Unset = UNSET,
    also: Literal["copies"] | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Document | ErrorEnvelope]:
    """Replace a document

     Replace a note's text (`application/json`: `body`, optionally `title`) or a file (`multipart/form-
    data`: `file`), keeping the document's id. It turns `processing` and keeps answering with its
    previous content until the new one is `ready`; a new file's name and size are the document's from
    then. A website is imported again (`application/json`: `pages`, or omit it to read again the pages
    it holds). A note can be replaced at any time, and a file again while its new version is still being
    read: the newer one takes its place. Refused (`document_not_ready`) for a file whose first upload is
    still `processing` or whose new version has been read and is about to replace the previous one, and
    for a website being imported; and (`conflict`) for a website whose location holds an older document
    of the same site. With `also=copies`, its copies at other locations get the same content, and the
    `document_not_ready` refusals apply to each copy. The JSON body is read as the document's kind: a
    field that kind does not take, such as `source`, or a note's `body` sent to a website, is refused
    (`invalid_parameter`) and nothing changes. Requires `knowledge:write`. Limited to 120 requests per
    minute per account (API key) or per installation (OAuth), and to 60 document writes per minute,
    shared by creating, replacing and updating documents and discovering a site's pages.

    Args:
        document_id (str):
        also (Literal['copies'] | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (DocumentReplace | DocumentSiteReplace):
        body (DocumentFileReplace): A file's new version, sent as `multipart/form-data`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Document | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
        body=body,
        also=also,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    document_id: str,
    *,
    client: AuthenticatedClient,
    body: DocumentReplace | DocumentSiteReplace | DocumentFileReplace | Unset = UNSET,
    also: Literal["copies"] | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Document | ErrorEnvelope | None:
    """Replace a document

     Replace a note's text (`application/json`: `body`, optionally `title`) or a file (`multipart/form-
    data`: `file`), keeping the document's id. It turns `processing` and keeps answering with its
    previous content until the new one is `ready`; a new file's name and size are the document's from
    then. A website is imported again (`application/json`: `pages`, or omit it to read again the pages
    it holds). A note can be replaced at any time, and a file again while its new version is still being
    read: the newer one takes its place. Refused (`document_not_ready`) for a file whose first upload is
    still `processing` or whose new version has been read and is about to replace the previous one, and
    for a website being imported; and (`conflict`) for a website whose location holds an older document
    of the same site. With `also=copies`, its copies at other locations get the same content, and the
    `document_not_ready` refusals apply to each copy. The JSON body is read as the document's kind: a
    field that kind does not take, such as `source`, or a note's `body` sent to a website, is refused
    (`invalid_parameter`) and nothing changes. Requires `knowledge:write`. Limited to 120 requests per
    minute per account (API key) or per installation (OAuth), and to 60 document writes per minute,
    shared by creating, replacing and updating documents and discovering a site's pages.

    Args:
        document_id (str):
        also (Literal['copies'] | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (DocumentReplace | DocumentSiteReplace):
        body (DocumentFileReplace): A file's new version, sent as `multipart/form-data`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Document | ErrorEnvelope
    """

    return sync_detailed(
        document_id=document_id,
        client=client,
        body=body,
        also=also,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    document_id: str,
    *,
    client: AuthenticatedClient,
    body: DocumentReplace | DocumentSiteReplace | DocumentFileReplace | Unset = UNSET,
    also: Literal["copies"] | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Document | ErrorEnvelope]:
    """Replace a document

     Replace a note's text (`application/json`: `body`, optionally `title`) or a file (`multipart/form-
    data`: `file`), keeping the document's id. It turns `processing` and keeps answering with its
    previous content until the new one is `ready`; a new file's name and size are the document's from
    then. A website is imported again (`application/json`: `pages`, or omit it to read again the pages
    it holds). A note can be replaced at any time, and a file again while its new version is still being
    read: the newer one takes its place. Refused (`document_not_ready`) for a file whose first upload is
    still `processing` or whose new version has been read and is about to replace the previous one, and
    for a website being imported; and (`conflict`) for a website whose location holds an older document
    of the same site. With `also=copies`, its copies at other locations get the same content, and the
    `document_not_ready` refusals apply to each copy. The JSON body is read as the document's kind: a
    field that kind does not take, such as `source`, or a note's `body` sent to a website, is refused
    (`invalid_parameter`) and nothing changes. Requires `knowledge:write`. Limited to 120 requests per
    minute per account (API key) or per installation (OAuth), and to 60 document writes per minute,
    shared by creating, replacing and updating documents and discovering a site's pages.

    Args:
        document_id (str):
        also (Literal['copies'] | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (DocumentReplace | DocumentSiteReplace):
        body (DocumentFileReplace): A file's new version, sent as `multipart/form-data`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Document | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
        body=body,
        also=also,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    document_id: str,
    *,
    client: AuthenticatedClient,
    body: DocumentReplace | DocumentSiteReplace | DocumentFileReplace | Unset = UNSET,
    also: Literal["copies"] | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Document | ErrorEnvelope | None:
    """Replace a document

     Replace a note's text (`application/json`: `body`, optionally `title`) or a file (`multipart/form-
    data`: `file`), keeping the document's id. It turns `processing` and keeps answering with its
    previous content until the new one is `ready`; a new file's name and size are the document's from
    then. A website is imported again (`application/json`: `pages`, or omit it to read again the pages
    it holds). A note can be replaced at any time, and a file again while its new version is still being
    read: the newer one takes its place. Refused (`document_not_ready`) for a file whose first upload is
    still `processing` or whose new version has been read and is about to replace the previous one, and
    for a website being imported; and (`conflict`) for a website whose location holds an older document
    of the same site. With `also=copies`, its copies at other locations get the same content, and the
    `document_not_ready` refusals apply to each copy. The JSON body is read as the document's kind: a
    field that kind does not take, such as `source`, or a note's `body` sent to a website, is refused
    (`invalid_parameter`) and nothing changes. Requires `knowledge:write`. Limited to 120 requests per
    minute per account (API key) or per installation (OAuth), and to 60 document writes per minute,
    shared by creating, replacing and updating documents and discovering a site's pages.

    Args:
        document_id (str):
        also (Literal['copies'] | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (DocumentReplace | DocumentSiteReplace):
        body (DocumentFileReplace): A file's new version, sent as `multipart/form-data`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Document | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            document_id=document_id,
            client=client,
            body=body,
            also=also,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
