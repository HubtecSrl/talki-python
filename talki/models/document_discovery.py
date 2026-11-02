from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DocumentDiscovery")


@_attrs_define
class DocumentDiscovery:
    """The pages found on a site, to choose the `pages` of an import from, and how many one import may read on the
    account's plan.

        Attributes:
            url (str): The address looked at.
            pages (list[str]): The site's pages found from its sitemap or its links, the address itself first.
            max_pages (int | None): How many pages one import may read on the account's plan; null when there is no limit.
    """

    url: str
    pages: list[str]
    max_pages: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        pages = self.pages

        max_pages: int | None
        max_pages = self.max_pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "pages": pages,
                "max_pages": max_pages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        pages = cast(list[str], d.pop("pages"))

        def _parse_max_pages(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_pages = _parse_max_pages(d.pop("max_pages"))

        document_discovery = cls(
            url=url,
            pages=pages,
            max_pages=max_pages,
        )

        document_discovery.additional_properties = d
        return document_discovery

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
