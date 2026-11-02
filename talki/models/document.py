from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.document_source import DocumentSource
from ..models.document_status import DocumentStatus

T = TypeVar("T", bound="Document")


@_attrs_define
class Document:
    """A document of the knowledge base the assistant answers callers from: a text note, an uploaded file or an imported
    website, at one location. Its copies at other locations are documents of their own, sharing `copy_group_id`. It is
    used once `status` is `ready`; a document whose content is replaced answers with its previous content until then.

        Attributes:
            id (str): Document identifier.
            location_id (str): The location whose assistant uses it (`GET /v1/locations`). Never null, and it never changes.
            title (str): The note's title, the uploaded file's name, or the imported site's address.
            source (DocumentSource): `text` for a note written as text, `file` for an uploaded file, `website` for pages
                imported from a site.
            mime_type (str): The content type: `text/markdown` for a note, the file's type for a file, `text/html` for a
                website.
            size_bytes (int): What it counts against the account's knowledge storage: the note's text, the file as uploaded,
                or the text extracted from the site. 0 for an upload that failed holding nothing.
            chunk_count (int): How many passages its content is searched as. While it is `processing`, the count of the
                content it still answers with; for a new document, 0 until its content has been read. A new copy may show its
                count from the start.
            file_available (bool): True when the uploaded file is kept and `GET /v1/documents/{document_id}/file` returns
                it: shortly after the file is first `ready`, later for a copy at another location. False for a note, a website,
                a file whose first upload is not `ready` yet or `failed`, and a file Talki did not keep. A file being replaced
                keeps its previous file until the new one has been read, then has none until shortly after the new version is
                `ready`.
            status (DocumentStatus): `processing` while its latest content is being read and indexed, `ready` once the
                assistant uses it, `failed` when its latest content could not be indexed (`status_error` says why). A document
                that was ready before keeps answering with its previous content while `processing` and after `failed`.
            status_error (None | str): Why its latest content could not be indexed. Null unless `status` is `failed`.
            enabled (bool): False when it is switched off: kept, but the assistant does not use it until it is switched on
                again.
            faq (bool): True for the location's FAQ note, which the answers taught with `POST
                /v1/unresolved_requests/{request_id}/teach` are added to. A location has one at most.
            copy_group_id (None | str): Shared by the copies of this document at other locations; null for a document that
                was never copied.
            created_at (datetime.datetime): RFC 3339 UTC.
            updated_at (datetime.datetime): When its title or content was last written, RFC 3339 UTC: a note's text or title
                when it is saved, a file's title when it is renamed, and a replaced file's or a website's new content, a dropped
                page included, when it is `ready`. Sending the same text, file or pages again counts as a write; switching it on
                or off does not.
    """

    id: str
    location_id: str
    title: str
    source: DocumentSource
    mime_type: str
    size_bytes: int
    chunk_count: int
    file_available: bool
    status: DocumentStatus
    status_error: None | str
    enabled: bool
    faq: bool
    copy_group_id: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        title = self.title

        source = self.source.value

        mime_type = self.mime_type

        size_bytes = self.size_bytes

        chunk_count = self.chunk_count

        file_available = self.file_available

        status = self.status.value

        status_error: None | str
        status_error = self.status_error

        enabled = self.enabled

        faq = self.faq

        copy_group_id: None | str
        copy_group_id = self.copy_group_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "title": title,
                "source": source,
                "mime_type": mime_type,
                "size_bytes": size_bytes,
                "chunk_count": chunk_count,
                "file_available": file_available,
                "status": status,
                "status_error": status_error,
                "enabled": enabled,
                "faq": faq,
                "copy_group_id": copy_group_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("location_id")

        title = d.pop("title")

        source = DocumentSource(d.pop("source"))

        mime_type = d.pop("mime_type")

        size_bytes = d.pop("size_bytes")

        chunk_count = d.pop("chunk_count")

        file_available = d.pop("file_available")

        status = DocumentStatus(d.pop("status"))

        def _parse_status_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        status_error = _parse_status_error(d.pop("status_error"))

        enabled = d.pop("enabled")

        faq = d.pop("faq")

        def _parse_copy_group_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        copy_group_id = _parse_copy_group_id(d.pop("copy_group_id"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        document = cls(
            id=id,
            location_id=location_id,
            title=title,
            source=source,
            mime_type=mime_type,
            size_bytes=size_bytes,
            chunk_count=chunk_count,
            file_available=file_available,
            status=status,
            status_error=status_error,
            enabled=enabled,
            faq=faq,
            copy_group_id=copy_group_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        document.additional_properties = d
        return document

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
