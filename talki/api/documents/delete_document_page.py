from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document_also import DocumentAlso
from ...models.error_envelope import ErrorEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    document_id: str,
    page_id: str,
    *,
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
        "method": "delete",
        "url": "/v1/documents/{document_id}/pages/{page_id}".format(
            document_id=quote(str(document_id), safe=""),
            page_id=quote(str(page_id), safe=""),
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


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    document_id: str,
    page_id: str,
    *,
    client: AuthenticatedClient,
    also: DocumentAlso | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Any | ErrorEnvelope]:
    """Delete a website's page

     Drop one page of an imported website and what it said; the assistant stops using it once the
    document is `ready` again. Dropping its last page that was read deletes the document
    (`document.deleted`). With `also=copies`, its copies at other locations get the result too. Only a
    website has pages; any other document is refused (`invalid_parameter`). Refused while the site is
    being imported (`document_not_ready`), and (`conflict`) when dropping it would leave no text to
    search while other pages are still listed as read: import the site again with the `pages` to keep,
    or delete the document. Requires `knowledge:write`. Limited to 120 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        document_id (str):
        page_id (str):
        also (DocumentAlso | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
        page_id=page_id,
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
    page_id: str,
    *,
    client: AuthenticatedClient,
    also: DocumentAlso | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Any | ErrorEnvelope | None:
    """Delete a website's page

     Drop one page of an imported website and what it said; the assistant stops using it once the
    document is `ready` again. Dropping its last page that was read deletes the document
    (`document.deleted`). With `also=copies`, its copies at other locations get the result too. Only a
    website has pages; any other document is refused (`invalid_parameter`). Refused while the site is
    being imported (`document_not_ready`), and (`conflict`) when dropping it would leave no text to
    search while other pages are still listed as read: import the site again with the `pages` to keep,
    or delete the document. Requires `knowledge:write`. Limited to 120 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        document_id (str):
        page_id (str):
        also (DocumentAlso | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorEnvelope
    """

    return sync_detailed(
        document_id=document_id,
        page_id=page_id,
        client=client,
        also=also,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    document_id: str,
    page_id: str,
    *,
    client: AuthenticatedClient,
    also: DocumentAlso | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[Any | ErrorEnvelope]:
    """Delete a website's page

     Drop one page of an imported website and what it said; the assistant stops using it once the
    document is `ready` again. Dropping its last page that was read deletes the document
    (`document.deleted`). With `also=copies`, its copies at other locations get the result too. Only a
    website has pages; any other document is refused (`invalid_parameter`). Refused while the site is
    being imported (`document_not_ready`), and (`conflict`) when dropping it would leave no text to
    search while other pages are still listed as read: import the site again with the `pages` to keep,
    or delete the document. Requires `knowledge:write`. Limited to 120 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        document_id (str):
        page_id (str):
        also (DocumentAlso | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
        page_id=page_id,
        also=also,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    document_id: str,
    page_id: str,
    *,
    client: AuthenticatedClient,
    also: DocumentAlso | None | Unset = UNSET,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Any | ErrorEnvelope | None:
    """Delete a website's page

     Drop one page of an imported website and what it said; the assistant stops using it once the
    document is `ready` again. Dropping its last page that was read deletes the document
    (`document.deleted`). With `also=copies`, its copies at other locations get the result too. Only a
    website has pages; any other document is refused (`invalid_parameter`). Refused while the site is
    being imported (`document_not_ready`), and (`conflict`) when dropping it would leave no text to
    search while other pages are still listed as read: import the site again with the `pages` to keep,
    or delete the document. Requires `knowledge:write`. Limited to 120 requests per minute per account
    (API key) or per installation (OAuth).

    Args:
        document_id (str):
        page_id (str):
        also (DocumentAlso | None | Unset): `copies` applies the change to every copy of the
            document at other locations too. Omit it to change only this document.
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            document_id=document_id,
            page_id=page_id,
            client=client,
            also=also,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
