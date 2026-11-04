"""`talki.documents` with three methods on top of the generated ones, for the
knowledge base's files: `upload` and `replace_file` send one as
`multipart/form-data` from a path, bytes or an open file, and `download`
returns one with the name and type it was uploaded with.

    document = talki.documents.upload("price-list.pdf")
    talki.documents.replace_file(document.id, "price-list-2027.pdf")
    file = talki.documents.download(document.id)
    Path(file.file_name or "download").write_bytes(file.payload.read())

`get_file`, which `download` is another name for, is the generated operation
with the file's name and type filled in from the answer's headers.

`Talki` and `AsyncTalki` expose these classes as `documents` in place of the
generated `DocumentsResource` and `AsyncDocumentsResource`, which they extend.
"""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from functools import cached_property
from io import BytesIO
from pathlib import Path, PureWindowsPath
from typing import IO, Any, Literal
from urllib.parse import unquote

import anyio.to_thread

from . import _resource
from .api import documents as _generated
from .api.documents import create_document, replace_document
from .models.document import Document
from .models.document_also import DocumentAlso
from .models.document_file_replace import DocumentFileReplace
from .models.document_upload import DocumentUpload
from .types import UNSET, File, Unset

__all__ = [
    "AsyncDocumentsResource",
    "AsyncDocumentsResourceWithRawResponse",
    "DocumentsResource",
    "DocumentsResourceWithRawResponse",
    "Upload",
]

# What `upload` and `replace_file` take: a path (a `str` is a path, never the
# content), the content as bytes, a file opened in binary mode, or a `File`.
Upload = str | os.PathLike[str] | bytes | IO[bytes] | File


# Reading what to send.


def _basename(name: object) -> str | None:
    """The last part of a path, with either separator, or None for no usable
    name: a name from elsewhere never points into another directory."""
    if not isinstance(name, str):
        return None
    base = PureWindowsPath(name).name.strip()
    return base if base not in ("", ".", "..") else None


def _read_io(stream: IO[bytes]) -> bytes:
    data: Any = stream.read()
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Open the file in binary mode ('rb'): its content is sent as bytes.")
    return bytes(data)


def _read(source: Upload) -> tuple[bytes, str | None, str | None]:
    """The bytes of ``source``, and the name and type it carries."""
    if isinstance(source, File):
        return _read_io(source.payload), source.file_name, source.mime_type
    if isinstance(source, (bytes, bytearray, memoryview)):
        return bytes(source), None, None
    if isinstance(source, (str, os.PathLike)):
        path = Path(source)
        return path.read_bytes(), path.name, None
    return _read_io(source), _basename(getattr(source, "name", None)), None


async def _aread(source: Upload) -> tuple[bytes, str | None, str | None]:
    """`_read`, reading a path on a worker thread."""
    if isinstance(source, (str, os.PathLike)):
        path = Path(source)
        return await anyio.to_thread.run_sync(path.read_bytes), path.name, None
    return _read(source)


def _file(read: tuple[bytes, str | None, str | None], filename: str | None, content_type: str | None) -> File:
    data, carried_name, carried_type = read
    name = filename if filename is not None else carried_name
    if not name:
        # Without a name the part is a form field, not a file, and the API
        # refuses it; the name is also the document's title.
        raise ValueError("The file needs a name, which becomes the document's title: pass filename=.")
    # With no type, httpx guesses one from the name, `application/octet-stream`
    # failing that, which the API types by the file's extension.
    return File(payload=BytesIO(data), file_name=name, mime_type=content_type or carried_type)


def _also(also: DocumentAlso | Literal["copies"] | None | Unset) -> DocumentAlso | None | Unset:
    """`replace_file`'s `also`, as the operation takes it: the plain string too."""
    return DocumentAlso(also) if isinstance(also, str) else also


def _no_none(location_ids: list[str] | None | Unset) -> list[str] | Unset:
    """`None` as no field at all: a form sends text, and the API's default is
    already none."""
    return UNSET if location_ids is None else location_ids


# Reading what came back.

# RFC 6266: `filename*` (RFC 8187, percent-encoded in a named charset) wins
# over the plain `filename`, which the API sends as an ASCII fallback.
_EXTENDED_NAME = re.compile(r"(?:^|;)\s*filename\*\s*=\s*([^';\s]*)'[^']*'([^;\s]*)", re.IGNORECASE)
_PLAIN_NAME = re.compile(r'(?:^|;)\s*filename\s*=\s*(?:"((?:[^"\\]|\\.)*)"|([^;\s]*))', re.IGNORECASE)


def filename_of(headers: Mapping[str, str]) -> str | None:
    """The file's name from a `Content-Disposition` header, its directories
    dropped, or None when it gives none."""
    value = next((v for k, v in headers.items() if k.lower() == "content-disposition"), None)
    if not value:
        return None
    extended = _EXTENDED_NAME.search(value)
    if extended:
        try:
            name = unquote(extended.group(2), encoding=extended.group(1) or "utf-8", errors="strict")
        except (LookupError, UnicodeDecodeError):
            pass
        else:
            if _basename(name):
                return _basename(name)
    plain = _PLAIN_NAME.search(value)
    if plain is None:
        return None
    quoted, token = plain.groups()
    return _basename(re.sub(r"\\(.)", r"\1", quoted) if quoted is not None else token)


def _media_type(headers: Mapping[str, str]) -> str | None:
    value = next((v for k, v in headers.items() if k.lower() == "content-type"), "")
    return value.split(";", 1)[0].strip().lower() or None


def _named(raw: _resource.RawResponse[File]) -> _resource.RawResponse[File]:
    """The downloaded `File` with the name and type its answer gives."""
    return raw.map(
        lambda file: File(payload=file.payload, file_name=filename_of(raw.headers), mime_type=_media_type(raw.headers))
    )


# Sync.


class DocumentsResourceWithRawResponse(_generated.DocumentsResourceWithRawResponse):
    """`talki.documents.with_raw_response`, with `upload`, `replace_file` and
    `download` too."""

    def upload(
        self,
        file: Upload,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        location_id: None | str | Unset = UNSET,
        location_ids: list[str] | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.upload`, returning the whole answer."""
        body = DocumentUpload(file=_file(_read(file), filename, content_type), location_ids=_no_none(location_ids))
        kwargs = create_document._get_kwargs(
            body=body, location_id=location_id, talki_version=talki_version, idempotency_key=idempotency_key
        )
        response = self._client.get_httpx_client().request(**kwargs)
        return _resource.raw(create_document._build_response(client=self._client, response=response))

    def replace_file(
        self,
        document_id: str,
        file: Upload,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        also: DocumentAlso | Literal["copies"] | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.replace_file`, returning the whole answer."""
        body = DocumentFileReplace(file=_file(_read(file), filename, content_type))
        kwargs = replace_document._get_kwargs(
            document_id, body=body, also=_also(also), talki_version=talki_version, idempotency_key=idempotency_key
        )
        response = self._client.get_httpx_client().request(**kwargs)
        return _resource.raw(replace_document._build_response(client=self._client, response=response))

    def get_file(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[File]:
        """`talki.documents.get_file`, returning the whole answer: the `File`
        with the name and type its answer gives."""
        return _named(super().get_file(document_id, talki_version=talki_version))

    def download(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[File]:
        """`talki.documents.download`, returning the whole answer."""
        return self.get_file(document_id, talki_version=talki_version)


class DocumentsResource(_generated.DocumentsResource):
    """`talki.documents`: the generated operations, and `upload`,
    `replace_file` and `download` for files."""

    @cached_property
    def with_raw_response(self) -> DocumentsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return DocumentsResourceWithRawResponse(self._client)

    def upload(
        self,
        file: Upload,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        location_id: None | str | Unset = UNSET,
        location_ids: list[str] | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Document:
        """Upload a file to the knowledge base: `POST /v1/documents` as
        `multipart/form-data`. Answers with the document still `processing`;
        `document.updated` says when it is `ready` or `failed`.

        Args:
            file: A path (a `str` is a path), the content as bytes, a file opened
                in binary mode, or a `talki.types.File`. It is read whole before
                sending (the API takes at most 10 MB, or less if the account's
                plan sets a lower limit), so a request turned away unrun is
                retried.
            filename: Its name, which becomes the document's `title`. Defaults to
                the path's, the open file's or the `File`'s; bytes need one.
            content_type: PDF, DOCX, XLSX, plain text or CSV. Defaults to the
                `File`'s, else one guessed from the name; the API types an
                unknown one by the extension.
            location_id: The location whose assistant uses it; the main one's
                when omitted.
            location_ids: Other locations that get a copy of it.
            talki_version: The `Talki-Version` for this request.
            idempotency_key: Required by the API; `Talki` adds one unless built
                with `auto_idempotency=False`.

        Raises:
            ValueError: No name could be found for the file.
            talki.ApiError: The API answered with an error, as the subclass for
                its `type`: `payload_too_large`, `unsupported_file_type`, …
        """
        return self.with_raw_response.upload(
            file,
            filename=filename,
            content_type=content_type,
            location_id=location_id,
            location_ids=location_ids,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        ).parse()

    def replace_file(
        self,
        document_id: str,
        file: Upload,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        also: DocumentAlso | Literal["copies"] | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Document:
        """Replace an uploaded file with a new version: `PUT
        /v1/documents/{document_id}` as `multipart/form-data`. The document
        keeps its id and answers with its previous content until the new one
        is `ready`; its `title` becomes the new name then.

        Takes ``file``, ``filename`` and ``content_type`` as `upload` does, and
        ``also="copies"`` to replace the file of every copy at other locations
        too. Refused with `409 document_not_ready` until the last file sent is
        in place: retry shortly.
        """
        return self.with_raw_response.replace_file(
            document_id,
            file,
            filename=filename,
            content_type=content_type,
            also=also,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        ).parse()

    def download(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> File:
        """An uploaded file as it was received: `GET
        /v1/documents/{document_id}/file`, as a `talki.types.File` with its
        `payload`, its `file_name` (directories dropped) and its `mime_type`.

        Only while the document's `file_available` is true; otherwise
        `404 resource_not_found`. The same as `get_file`.
        """
        return self.with_raw_response.download(document_id, talki_version=talki_version).parse()


# Async.


class AsyncDocumentsResourceWithRawResponse(_generated.AsyncDocumentsResourceWithRawResponse):
    """`talki.documents.with_raw_response` on `AsyncTalki`, with `upload`,
    `replace_file` and `download` too."""

    async def upload(
        self,
        file: Upload,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        location_id: None | str | Unset = UNSET,
        location_ids: list[str] | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.upload`, returning the whole answer."""
        body = DocumentUpload(
            file=_file(await _aread(file), filename, content_type), location_ids=_no_none(location_ids)
        )
        kwargs = create_document._get_kwargs(
            body=body, location_id=location_id, talki_version=talki_version, idempotency_key=idempotency_key
        )
        response = await self._client.get_async_httpx_client().request(**kwargs)
        return _resource.raw(create_document._build_response(client=self._client, response=response))

    async def replace_file(
        self,
        document_id: str,
        file: Upload,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        also: DocumentAlso | Literal["copies"] | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Document]:
        """`talki.documents.replace_file`, returning the whole answer."""
        body = DocumentFileReplace(file=_file(await _aread(file), filename, content_type))
        kwargs = replace_document._get_kwargs(
            document_id, body=body, also=_also(also), talki_version=talki_version, idempotency_key=idempotency_key
        )
        response = await self._client.get_async_httpx_client().request(**kwargs)
        return _resource.raw(replace_document._build_response(client=self._client, response=response))

    async def get_file(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[File]:
        """`talki.documents.get_file`, returning the whole answer: the `File`
        with the name and type its answer gives."""
        return _named(await super().get_file(document_id, talki_version=talki_version))

    async def download(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[File]:
        """`talki.documents.download`, returning the whole answer."""
        return await self.get_file(document_id, talki_version=talki_version)


class AsyncDocumentsResource(_generated.AsyncDocumentsResource):
    """`talki.documents` on `AsyncTalki`: the generated operations, and
    `upload`, `replace_file` and `download` for files."""

    @cached_property
    def with_raw_response(self) -> AsyncDocumentsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncDocumentsResourceWithRawResponse(self._client)

    async def upload(
        self,
        file: Upload,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        location_id: None | str | Unset = UNSET,
        location_ids: list[str] | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Document:
        """`Talki`'s `documents.upload`, awaited. A path is read on a worker
        thread."""
        return (
            await self.with_raw_response.upload(
                file,
                filename=filename,
                content_type=content_type,
                location_id=location_id,
                location_ids=location_ids,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def replace_file(
        self,
        document_id: str,
        file: Upload,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        also: DocumentAlso | Literal["copies"] | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Document:
        """`Talki`'s `documents.replace_file`, awaited."""
        return (
            await self.with_raw_response.replace_file(
                document_id,
                file,
                filename=filename,
                content_type=content_type,
                also=also,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def download(
        self,
        document_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> File:
        """`Talki`'s `documents.download`, awaited."""
        return (await self.with_raw_response.download(document_id, talki_version=talki_version)).parse()
