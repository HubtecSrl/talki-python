from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Literal, Required, TypedDict, TypeVar, cast

from attrs import define as _attrs_define

from ..models.document_create_source import DocumentCreateSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentCreate")


@_attrs_define
class DocumentCreate:
    """A text note, sent as `application/json`. Its title and text are what the assistant reads.

    Attributes:
        title (str): Its title, at most 200 characters. The assistant reads it too.
        body (str): Its text, at most 100 KB in UTF-8. Plain text or Markdown.
        source (DocumentCreateSource | Unset): `text`, or omit it. A website is sent with `website`. Default:
            DocumentCreateSource.TEXT.
        location_ids (list[str] | None | Unset): Other locations that get a copy of it, ids from `GET /v1/locations`.
            Each copy is a document of its own, sharing `copy_group_id`.
    """

    title: str
    body: str
    source: DocumentCreateSource | Unset = DocumentCreateSource.TEXT
    location_ids: list[str] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        body = self.body

        source: str | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        location_ids: list[str] | None | Unset
        if isinstance(self.location_ids, Unset):
            location_ids = UNSET
        elif isinstance(self.location_ids, list):
            location_ids = self.location_ids

        else:
            location_ids = self.location_ids

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "title": title,
                "body": body,
            }
        )
        if source is not UNSET:
            field_dict["source"] = source
        if location_ids is not UNSET:
            field_dict["location_ids"] = location_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        body = d.pop("body")

        _source = d.pop("source", UNSET)
        source: DocumentCreateSource | Unset
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = DocumentCreateSource(_source)

        def _parse_location_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                location_ids_type_0 = cast(list[str], data)

                return location_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        location_ids = _parse_location_ids(d.pop("location_ids", UNSET))

        document_create = cls(
            title=title,
            body=body,
            source=source,
            location_ids=location_ids,
        )

        return document_create


# `DocumentCreate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class DocumentCreateDict(TypedDict, total=False):
    title: Required[str]
    body: Required[str]
    source: DocumentCreateSource | Literal["text"]
    location_ids: Sequence[str] | None
