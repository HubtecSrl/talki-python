from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document import Document
from ...models.document_also import DocumentAlso
from ...models.document_update import DocumentUpdate
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    document_id: str,
    *,
    body: DocumentUpdate,
    also: DocumentAlso | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    params: dict[str, Any] = {}

    json_also: None | str | Unset
    if isinstance(also, Unset):
        json_also = UNSET
    elif isinstance(also, DocumentAlso):
        json_also = also.value
    else:
        json_also = also
    params["also"] = json_also

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/documents/{document_id}".format(
            document_id=quote(str(document_id), safe=""),
        ),
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
) -> Document | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = Document.from_dict(response.json())

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
    body: DocumentUpdate,
    also: DocumentAlso | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Document | ErrorEnvelope]:
    """Update a document

     Rename a document, or switch it off (`enabled: false`) so the assistant stops using it while it is
    kept, and on again. A note's new title is indexed again, as its text is. A file's title cannot
    change while it is `processing` (`document_not_ready`). A website's title is its address and cannot
    change. With `also=copies`, its copies at other locations change too, and a rename is refused the
    same way (`document_not_ready`) while a copy's file is `processing`. Any other field is refused
    (`invalid_parameter`). A request that changes nothing sends no `document.updated`. Requires
    `knowledge:write`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth), and to 60 document writes per minute, shared by creating, replacing and updating documents
    and discovering a site's pages.

    Args:
        document_id (str):
        also (DocumentAlso | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (DocumentUpdate): A partial edit of a document: its title, or whether the assistant
            uses it.

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
    body: DocumentUpdate,
    also: DocumentAlso | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Document | ErrorEnvelope | None:
    """Update a document

     Rename a document, or switch it off (`enabled: false`) so the assistant stops using it while it is
    kept, and on again. A note's new title is indexed again, as its text is. A file's title cannot
    change while it is `processing` (`document_not_ready`). A website's title is its address and cannot
    change. With `also=copies`, its copies at other locations change too, and a rename is refused the
    same way (`document_not_ready`) while a copy's file is `processing`. Any other field is refused
    (`invalid_parameter`). A request that changes nothing sends no `document.updated`. Requires
    `knowledge:write`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth), and to 60 document writes per minute, shared by creating, replacing and updating documents
    and discovering a site's pages.

    Args:
        document_id (str):
        also (DocumentAlso | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (DocumentUpdate): A partial edit of a document: its title, or whether the assistant
            uses it.

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
    body: DocumentUpdate,
    also: DocumentAlso | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Document | ErrorEnvelope]:
    """Update a document

     Rename a document, or switch it off (`enabled: false`) so the assistant stops using it while it is
    kept, and on again. A note's new title is indexed again, as its text is. A file's title cannot
    change while it is `processing` (`document_not_ready`). A website's title is its address and cannot
    change. With `also=copies`, its copies at other locations change too, and a rename is refused the
    same way (`document_not_ready`) while a copy's file is `processing`. Any other field is refused
    (`invalid_parameter`). A request that changes nothing sends no `document.updated`. Requires
    `knowledge:write`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth), and to 60 document writes per minute, shared by creating, replacing and updating documents
    and discovering a site's pages.

    Args:
        document_id (str):
        also (DocumentAlso | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (DocumentUpdate): A partial edit of a document: its title, or whether the assistant
            uses it.

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
    body: DocumentUpdate,
    also: DocumentAlso | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Document | ErrorEnvelope | None:
    """Update a document

     Rename a document, or switch it off (`enabled: false`) so the assistant stops using it while it is
    kept, and on again. A note's new title is indexed again, as its text is. A file's title cannot
    change while it is `processing` (`document_not_ready`). A website's title is its address and cannot
    change. With `also=copies`, its copies at other locations change too, and a rename is refused the
    same way (`document_not_ready`) while a copy's file is `processing`. Any other field is refused
    (`invalid_parameter`). A request that changes nothing sends no `document.updated`. Requires
    `knowledge:write`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth), and to 60 document writes per minute, shared by creating, replacing and updating documents
    and discovering a site's pages.

    Args:
        document_id (str):
        also (DocumentAlso | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):
        body (DocumentUpdate): A partial edit of a document: its title, or whether the assistant
            uses it.

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
