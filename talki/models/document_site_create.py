from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Literal, Required, TypedDict, TypeVar, cast

from attrs import define as _attrs_define

from ..models.document_site_create_source import DocumentSiteCreateSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentSiteCreate")


@_attrs_define
class DocumentSiteCreate:
    """A website to import, sent as `application/json` with `source: "website"`: the page at `url`, or the `pages` listed,
    up to the plan's page limit.

        Attributes:
            source (DocumentSiteCreateSource): `website`.
            url (str): The site's address, http or https. It becomes the document's `title`.
            pages (list[str] | None | Unset): The pages to read, from `POST /v1/documents/discover` or your own, at most the
                account plan's page limit. Omit to read the page at `url` alone.
            location_ids (list[str] | None | Unset): Other locations that get a copy of it, ids from `GET /v1/locations`.
                Each copy is a document of its own, sharing `copy_group_id`.
    """

    source: DocumentSiteCreateSource
    url: str
    pages: list[str] | None | Unset = UNSET
    location_ids: list[str] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        source = self.source.value

        url = self.url

        pages: list[str] | None | Unset
        if isinstance(self.pages, Unset):
            pages = UNSET
        elif isinstance(self.pages, list):
            pages = self.pages

        else:
            pages = self.pages

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
                "source": source,
                "url": url,
            }
        )
        if pages is not UNSET:
            field_dict["pages"] = pages
        if location_ids is not UNSET:
            field_dict["location_ids"] = location_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = DocumentSiteCreateSource(d.pop("source"))

        url = d.pop("url")

        def _parse_pages(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                pages_type_0 = cast(list[str], data)

                return pages_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        pages = _parse_pages(d.pop("pages", UNSET))

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

        document_site_create = cls(
            source=source,
            url=url,
            pages=pages,
            location_ids=location_ids,
        )

        return document_site_create


# `DocumentSiteCreate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class DocumentSiteCreateDict(TypedDict, total=False):
    source: Required[DocumentSiteCreateSource | Literal["website"]]
    url: Required[str]
    pages: Sequence[str] | None
    location_ids: Sequence[str] | None
