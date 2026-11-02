from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.document_page_status import DocumentPageStatus

T = TypeVar("T", bound="DocumentPage")


@_attrs_define
class DocumentPage:
    """One page of an imported website, and whether it was read.

    Attributes:
        id (str): Page identifier.
        url (str): The page's address.
        title (None | str): The page's title, when it has one.
        status (DocumentPageStatus): `ok` when it was read, `thin` when it was read but holds little text, `blocked`
            when the site refused it (bot protection), `failed` when it could not be read. Only `ok` and `thin` pages are
            searched.
        char_count (int): Characters of text read from it.
        crawled_at (datetime.datetime | None): When it was read, RFC 3339 UTC.
    """

    id: str
    url: str
    title: None | str
    status: DocumentPageStatus
    char_count: int
    crawled_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        url = self.url

        title: None | str
        title = self.title

        status = self.status.value

        char_count = self.char_count

        crawled_at: None | str
        if isinstance(self.crawled_at, datetime.datetime):
            crawled_at = self.crawled_at.isoformat()
        else:
            crawled_at = self.crawled_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "url": url,
                "title": title,
                "status": status,
                "char_count": char_count,
                "crawled_at": crawled_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        url = d.pop("url")

        def _parse_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        title = _parse_title(d.pop("title"))

        status = DocumentPageStatus(d.pop("status"))

        char_count = d.pop("char_count")

        def _parse_crawled_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                crawled_at_type_0 = datetime.datetime.fromisoformat(data)

                return crawled_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        crawled_at = _parse_crawled_at(d.pop("crawled_at"))

        document_page = cls(
            id=id,
            url=url,
            title=title,
            status=status,
            char_count=char_count,
            crawled_at=crawled_at,
        )

        document_page.additional_properties = d
        return document_page

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
