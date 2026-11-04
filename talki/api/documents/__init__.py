"""The `documents` operations, one module each, and `DocumentsResource` / `AsyncDocumentsResource`,
which `Talki` and `AsyncTalki` expose as `documents`."""

from functools import cached_property

from ... import _resource
from ... import pagination as _pagination
from ...models.delete_document_also_type_0 import DeleteDocumentAlsoType0
from ...models.delete_document_page_also_type_0 import DeleteDocumentPageAlsoType0
from ...models.document import Document
from ...models.document_create import DocumentCreate
from ...models.document_discover import DocumentDiscover, DocumentDiscoverDict
from ...models.document_discovery import DocumentDiscovery
from ...models.document_file_replace import DocumentFileReplace
from ...models.document_list import DocumentList
from ...models.document_page_list import DocumentPageList
from ...models.document_replace import DocumentReplace
from ...models.document_site_create import DocumentSiteCreate
from ...models.document_site_replace import DocumentSiteReplace
from ...models.document_text import DocumentText
from ...models.document_update import DocumentUpdate, DocumentUpdateDict
from ...models.document_upload import DocumentUpload
from ...models.list_documents_source_type_0 import ListDocumentsSourceType0
from ...models.replace_document_also_type_0 import ReplaceDocumentAlsoType0
from ...models.update_document_also_type_0 import UpdateDocumentAlsoType0
from ...types import UNSET, File, Unset
from . import (
    create_document,
    delete_document,
    delete_document_page,
    discover_document_pages,
    get_document,
    get_document_file,
    get_document_text,
    list_document_pages,
    list_documents,
    replace_document,
    update_document,
)

__all__ = [
    "AsyncDocumentsResource",
    "AsyncDocumentsResourceWithRawResponse",
    "DocumentsResource",
    "DocumentsResourceWithRawResponse",
]


class DocumentsResourceWithRawResponse(_resource.Resource):
    """`talki.documents.with_raw_response`: the methods of `talki.documents`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def create(
        self,
        *,
        body: DocumentCreate | DocumentSiteCreate | DocumentUpload | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.create`, returning the whole answer."""
        return _resource.raw(
            create_document.sync_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def delete(
        self,
        document_id: str,
        *,
        also: DeleteDocumentAlsoType0 | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.documents.delete`, returning the whole answer."""
        return _resource.raw(
            delete_document.sync_detailed(
                client=self._client,
                document_id=document_id,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def delete_page(
        self,
        document_id: str,
        page_id: str,
        *,
        also: DeleteDocumentPageAlsoType0 | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.documents.delete_page`, returning the whole answer."""
        return _resource.raw(
            delete_document_page.sync_detailed(
                client=self._client,
                document_id=document_id,
                page_id=page_id,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def discover_pages(
        self,
        *,
        body: DocumentDiscover | DocumentDiscoverDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[DocumentDiscovery]:
        """`talki.documents.discover_pages`, returning the whole answer."""
        body = _resource.as_body(body, DocumentDiscover)
        return _resource.raw(
            discover_document_pages.sync_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def get(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.get`, returning the whole answer."""
        return _resource.raw(
            get_document.sync_detailed(
                client=self._client,
                document_id=document_id,
                talki_version=talki_version,
            )
        )

    def get_file(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[File]:
        """`talki.documents.get_file`, returning the whole answer."""
        return _resource.raw(
            get_document_file.sync_detailed(
                client=self._client,
                document_id=document_id,
                talki_version=talki_version,
            )
        )

    def get_text(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[DocumentText]:
        """`talki.documents.get_text`, returning the whole answer."""
        return _resource.raw(
            get_document_text.sync_detailed(
                client=self._client,
                document_id=document_id,
                talki_version=talki_version,
            )
        )

    def list_pages(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[DocumentPageList]:
        """`talki.documents.list_pages`, returning the whole answer."""
        return _resource.raw(
            list_document_pages.sync_detailed(
                client=self._client,
                document_id=document_id,
                talki_version=talki_version,
            )
        )

    def replace(
        self,
        document_id: str,
        *,
        body: DocumentReplace | DocumentSiteReplace | DocumentFileReplace | Unset = UNSET,
        also: None | ReplaceDocumentAlsoType0 | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.replace`, returning the whole answer."""
        return _resource.raw(
            replace_document.sync_detailed(
                client=self._client,
                document_id=document_id,
                body=body,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def update(
        self,
        document_id: str,
        *,
        body: DocumentUpdate | DocumentUpdateDict,
        also: None | Unset | UpdateDocumentAlsoType0 = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.update`, returning the whole answer."""
        body = _resource.as_body(body, DocumentUpdate)
        return _resource.raw(
            update_document.sync_detailed(
                client=self._client,
                document_id=document_id,
                body=body,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        source: ListDocumentsSourceType0 | None | Unset = UNSET,
        enabled: bool | None | Unset = UNSET,
        faq: bool | None | Unset = UNSET,
        copy_group_id: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.Page[Document]]:
        """`talki.documents.list`, returning the whole answer."""

        def fetch(cursor: None | str | Unset) -> DocumentList:
            return _resource.unwrap(
                list_documents.sync_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    source=source,
                    enabled=enabled,
                    faq=faq,
                    copy_group_id=copy_group_id,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            list_documents.sync_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                source=source,
                enabled=enabled,
                faq=faq,
                copy_group_id=copy_group_id,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.Page(page, fetch, cursor))


class DocumentsResource(_resource.Resource):
    """`talki.documents`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> DocumentsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return DocumentsResourceWithRawResponse(self._client)

    def create(
        self,
        *,
        body: DocumentCreate | DocumentSiteCreate | DocumentUpload | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Document:
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
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (DocumentCreate | DocumentSiteCreate):
            body (DocumentUpload): A file, sent as `multipart/form-data`: PDF, DOCX, XLSX, TXT or CSV,
                at most 10 MB or the plan's lower limit.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Document
        """
        return (
            self.with_raw_response.create(
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def delete(
        self,
        document_id: str,
        *,
        also: DeleteDocumentAlsoType0 | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a document

         Delete a document for good; the assistant stops using it at once. A location's FAQ note can be
        deleted too: the next answer taught there starts a new one. With `also=copies`, its copies at other
        locations go too; without it they stay. Sends `document.deleted`. Requires `knowledge:write`.
        Limited to 120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            document_id (str):
            also (DeleteDocumentAlsoType0 | None | Unset): `copies` applies the change to every copy
                of the document at other locations too. Omit it to change only this document.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            self.with_raw_response.delete(
                document_id=document_id,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def delete_page(
        self,
        document_id: str,
        page_id: str,
        *,
        also: DeleteDocumentPageAlsoType0 | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
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
            also (DeleteDocumentPageAlsoType0 | None | Unset): `copies` applies the change to every
                copy of the document at other locations too. Omit it to change only this document.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            self.with_raw_response.delete_page(
                document_id=document_id,
                page_id=page_id,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def discover_pages(
        self,
        *,
        body: DocumentDiscover | DocumentDiscoverDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> DocumentDiscovery:
        """Discover a site's pages

         Look for the pages of the site at `url`, from its sitemap or its links, to choose the `pages` of an
        import. Imports nothing. `max_pages` is how many one import may read on the account's plan. An
        address that is not public http or https, or any field besides `url`, is refused
        (`invalid_parameter`). Requires `knowledge:write`. Limited to 120 requests per minute per account
        (API key) or per installation (OAuth), and to 60 document writes per minute, shared by creating,
        replacing and updating documents and discovering a site's pages.

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (DocumentDiscover | DocumentDiscoverDict): A site to look for pages in before importing it.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            DocumentDiscovery
        """
        return (
            self.with_raw_response.discover_pages(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def get(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Document:
        """Retrieve a document

         Return one document of the account, with its indexing `status`. Requires `knowledge:read`. Limited
        to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            document_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Document
        """
        return (
            self.with_raw_response.get(
                document_id=document_id,
                talki_version=talki_version,
            )
        ).parse()

    def get_file(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> File:
        """Download a document's file

         Return the uploaded file as it was received, with its type and name, when the document's
        `file_available` is true: shortly after the file is first `ready`, later for a copy at another
        location. A note, a website, a file whose first upload is not `ready` yet or `failed`, and a file
        Talki did not keep have none (`resource_not_found`). A file being replaced returns its previous
        version until the new one has been read, then its new version shortly after it is `ready`. Requires
        `knowledge:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            document_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            File
        """
        return (
            self.with_raw_response.get_file(
                document_id=document_id,
                talki_version=talki_version,
            )
        ).parse()

    def get_text(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> DocumentText:
        """Retrieve a document's text

         Return a note's text as last written, even while it is `processing`, or the text Talki read from a
        file or a website, as the assistant searches it: empty until the file or website is first `ready`.
        The uploaded file itself is `GET /v1/documents/{document_id}/file`. Requires `knowledge:read`.
        Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            document_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            DocumentText
        """
        return (
            self.with_raw_response.get_text(
                document_id=document_id,
                talki_version=talki_version,
            )
        ).parse()

    def list_pages(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> DocumentPageList:
        """List a website's pages

         Return every page of an imported website as its last import read them, with whether each was read
        (`status`). Only a website has pages; any other document is refused (`invalid_parameter`). Requires
        `knowledge:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            document_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            DocumentPageList
        """
        return (
            self.with_raw_response.list_pages(
                document_id=document_id,
                talki_version=talki_version,
            )
        ).parse()

    def replace(
        self,
        document_id: str,
        *,
        body: DocumentReplace | DocumentSiteReplace | DocumentFileReplace | Unset = UNSET,
        also: None | ReplaceDocumentAlsoType0 | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Document:
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
            also (None | ReplaceDocumentAlsoType0 | Unset): `copies` applies the change to every copy
                of the document at other locations too. Omit it to change only this document.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (DocumentReplace | DocumentSiteReplace):
            body (DocumentFileReplace): A file's new version, sent as `multipart/form-data`.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Document
        """
        return (
            self.with_raw_response.replace(
                document_id=document_id,
                body=body,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def update(
        self,
        document_id: str,
        *,
        body: DocumentUpdate | DocumentUpdateDict,
        also: None | Unset | UpdateDocumentAlsoType0 = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Document:
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
            also (None | Unset | UpdateDocumentAlsoType0): `copies` applies the change to every copy
                of the document at other locations too. Omit it to change only this document.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (DocumentUpdate | DocumentUpdateDict): A partial edit of a document: its title, or whether the assistant
                uses it.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Document
        """
        return (
            self.with_raw_response.update(
                document_id=document_id,
                body=body,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        source: ListDocumentsSourceType0 | None | Unset = UNSET,
        enabled: bool | None | Unset = UNSET,
        faq: bool | None | Unset = UNSET,
        copy_group_id: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[Document]:
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
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Page[Document]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """
        return (
            self.with_raw_response.list(
                limit=limit,
                cursor=cursor,
                source=source,
                enabled=enabled,
                faq=faq,
                copy_group_id=copy_group_id,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()


class AsyncDocumentsResourceWithRawResponse(_resource.Resource):
    """`talki.documents.with_raw_response` on `AsyncTalki`: the methods of `talki.documents`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def create(
        self,
        *,
        body: DocumentCreate | DocumentSiteCreate | DocumentUpload | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.create`, returning the whole answer."""
        return _resource.raw(
            await create_document.asyncio_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def delete(
        self,
        document_id: str,
        *,
        also: DeleteDocumentAlsoType0 | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.documents.delete`, returning the whole answer."""
        return _resource.raw(
            await delete_document.asyncio_detailed(
                client=self._client,
                document_id=document_id,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def delete_page(
        self,
        document_id: str,
        page_id: str,
        *,
        also: DeleteDocumentPageAlsoType0 | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.documents.delete_page`, returning the whole answer."""
        return _resource.raw(
            await delete_document_page.asyncio_detailed(
                client=self._client,
                document_id=document_id,
                page_id=page_id,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def discover_pages(
        self,
        *,
        body: DocumentDiscover | DocumentDiscoverDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[DocumentDiscovery]:
        """`talki.documents.discover_pages`, returning the whole answer."""
        body = _resource.as_body(body, DocumentDiscover)
        return _resource.raw(
            await discover_document_pages.asyncio_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def get(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.get`, returning the whole answer."""
        return _resource.raw(
            await get_document.asyncio_detailed(
                client=self._client,
                document_id=document_id,
                talki_version=talki_version,
            )
        )

    async def get_file(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[File]:
        """`talki.documents.get_file`, returning the whole answer."""
        return _resource.raw(
            await get_document_file.asyncio_detailed(
                client=self._client,
                document_id=document_id,
                talki_version=talki_version,
            )
        )

    async def get_text(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[DocumentText]:
        """`talki.documents.get_text`, returning the whole answer."""
        return _resource.raw(
            await get_document_text.asyncio_detailed(
                client=self._client,
                document_id=document_id,
                talki_version=talki_version,
            )
        )

    async def list_pages(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[DocumentPageList]:
        """`talki.documents.list_pages`, returning the whole answer."""
        return _resource.raw(
            await list_document_pages.asyncio_detailed(
                client=self._client,
                document_id=document_id,
                talki_version=talki_version,
            )
        )

    async def replace(
        self,
        document_id: str,
        *,
        body: DocumentReplace | DocumentSiteReplace | DocumentFileReplace | Unset = UNSET,
        also: None | ReplaceDocumentAlsoType0 | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.replace`, returning the whole answer."""
        return _resource.raw(
            await replace_document.asyncio_detailed(
                client=self._client,
                document_id=document_id,
                body=body,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def update(
        self,
        document_id: str,
        *,
        body: DocumentUpdate | DocumentUpdateDict,
        also: None | Unset | UpdateDocumentAlsoType0 = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.update`, returning the whole answer."""
        body = _resource.as_body(body, DocumentUpdate)
        return _resource.raw(
            await update_document.asyncio_detailed(
                client=self._client,
                document_id=document_id,
                body=body,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        source: ListDocumentsSourceType0 | None | Unset = UNSET,
        enabled: bool | None | Unset = UNSET,
        faq: bool | None | Unset = UNSET,
        copy_group_id: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.AsyncPage[Document]]:
        """`talki.documents.list`, returning the whole answer."""

        async def fetch(cursor: None | str | Unset) -> DocumentList:
            return _resource.unwrap(
                await list_documents.asyncio_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    source=source,
                    enabled=enabled,
                    faq=faq,
                    copy_group_id=copy_group_id,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            await list_documents.asyncio_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                source=source,
                enabled=enabled,
                faq=faq,
                copy_group_id=copy_group_id,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.AsyncPage(page, fetch, cursor))


class AsyncDocumentsResource(_resource.Resource):
    """`talki.documents` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncDocumentsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncDocumentsResourceWithRawResponse(self._client)

    async def create(
        self,
        *,
        body: DocumentCreate | DocumentSiteCreate | DocumentUpload | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Document:
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
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (DocumentCreate | DocumentSiteCreate):
            body (DocumentUpload): A file, sent as `multipart/form-data`: PDF, DOCX, XLSX, TXT or CSV,
                at most 10 MB or the plan's lower limit.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Document
        """
        return (
            await self.with_raw_response.create(
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def delete(
        self,
        document_id: str,
        *,
        also: DeleteDocumentAlsoType0 | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a document

         Delete a document for good; the assistant stops using it at once. A location's FAQ note can be
        deleted too: the next answer taught there starts a new one. With `also=copies`, its copies at other
        locations go too; without it they stay. Sends `document.deleted`. Requires `knowledge:write`.
        Limited to 120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            document_id (str):
            also (DeleteDocumentAlsoType0 | None | Unset): `copies` applies the change to every copy
                of the document at other locations too. Omit it to change only this document.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            await self.with_raw_response.delete(
                document_id=document_id,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def delete_page(
        self,
        document_id: str,
        page_id: str,
        *,
        also: DeleteDocumentPageAlsoType0 | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
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
            also (DeleteDocumentPageAlsoType0 | None | Unset): `copies` applies the change to every
                copy of the document at other locations too. Omit it to change only this document.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            await self.with_raw_response.delete_page(
                document_id=document_id,
                page_id=page_id,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def discover_pages(
        self,
        *,
        body: DocumentDiscover | DocumentDiscoverDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> DocumentDiscovery:
        """Discover a site's pages

         Look for the pages of the site at `url`, from its sitemap or its links, to choose the `pages` of an
        import. Imports nothing. `max_pages` is how many one import may read on the account's plan. An
        address that is not public http or https, or any field besides `url`, is refused
        (`invalid_parameter`). Requires `knowledge:write`. Limited to 120 requests per minute per account
        (API key) or per installation (OAuth), and to 60 document writes per minute, shared by creating,
        replacing and updating documents and discovering a site's pages.

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (DocumentDiscover | DocumentDiscoverDict): A site to look for pages in before importing it.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            DocumentDiscovery
        """
        return (
            await self.with_raw_response.discover_pages(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def get(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Document:
        """Retrieve a document

         Return one document of the account, with its indexing `status`. Requires `knowledge:read`. Limited
        to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            document_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Document
        """
        return (
            await self.with_raw_response.get(
                document_id=document_id,
                talki_version=talki_version,
            )
        ).parse()

    async def get_file(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> File:
        """Download a document's file

         Return the uploaded file as it was received, with its type and name, when the document's
        `file_available` is true: shortly after the file is first `ready`, later for a copy at another
        location. A note, a website, a file whose first upload is not `ready` yet or `failed`, and a file
        Talki did not keep have none (`resource_not_found`). A file being replaced returns its previous
        version until the new one has been read, then its new version shortly after it is `ready`. Requires
        `knowledge:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            document_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            File
        """
        return (
            await self.with_raw_response.get_file(
                document_id=document_id,
                talki_version=talki_version,
            )
        ).parse()

    async def get_text(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> DocumentText:
        """Retrieve a document's text

         Return a note's text as last written, even while it is `processing`, or the text Talki read from a
        file or a website, as the assistant searches it: empty until the file or website is first `ready`.
        The uploaded file itself is `GET /v1/documents/{document_id}/file`. Requires `knowledge:read`.
        Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            document_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            DocumentText
        """
        return (
            await self.with_raw_response.get_text(
                document_id=document_id,
                talki_version=talki_version,
            )
        ).parse()

    async def list_pages(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> DocumentPageList:
        """List a website's pages

         Return every page of an imported website as its last import read them, with whether each was read
        (`status`). Only a website has pages; any other document is refused (`invalid_parameter`). Requires
        `knowledge:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            document_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            DocumentPageList
        """
        return (
            await self.with_raw_response.list_pages(
                document_id=document_id,
                talki_version=talki_version,
            )
        ).parse()

    async def replace(
        self,
        document_id: str,
        *,
        body: DocumentReplace | DocumentSiteReplace | DocumentFileReplace | Unset = UNSET,
        also: None | ReplaceDocumentAlsoType0 | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Document:
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
            also (None | ReplaceDocumentAlsoType0 | Unset): `copies` applies the change to every copy
                of the document at other locations too. Omit it to change only this document.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (DocumentReplace | DocumentSiteReplace):
            body (DocumentFileReplace): A file's new version, sent as `multipart/form-data`.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Document
        """
        return (
            await self.with_raw_response.replace(
                document_id=document_id,
                body=body,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def update(
        self,
        document_id: str,
        *,
        body: DocumentUpdate | DocumentUpdateDict,
        also: None | Unset | UpdateDocumentAlsoType0 = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Document:
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
            also (None | Unset | UpdateDocumentAlsoType0): `copies` applies the change to every copy
                of the document at other locations too. Omit it to change only this document.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (DocumentUpdate | DocumentUpdateDict): A partial edit of a document: its title, or whether the assistant
                uses it.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Document
        """
        return (
            await self.with_raw_response.update(
                document_id=document_id,
                body=body,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        source: ListDocumentsSourceType0 | None | Unset = UNSET,
        enabled: bool | None | Unset = UNSET,
        faq: bool | None | Unset = UNSET,
        copy_group_id: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPager[Document]:
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
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AsyncPager[Document]: Awaited, this page (an `AsyncPage`). Iterated with `async for`,
            every row from here on, fetching the pages as it goes.
        """

        async def first() -> _pagination.AsyncPage[Document]:
            return (
                await self.with_raw_response.list(
                    limit=limit,
                    cursor=cursor,
                    source=source,
                    enabled=enabled,
                    faq=faq,
                    copy_group_id=copy_group_id,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            ).parse()

        return _pagination.AsyncPager(first)
