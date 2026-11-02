from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Required, TypedDict, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DocumentDiscover")


@_attrs_define
class DocumentDiscover:
    """A site to look for pages in before importing it.

    Attributes:
        url (str): The site's address, http or https.
    """

    url: str

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        document_discover = cls(
            url=url,
        )

        return document_discover


# `DocumentDiscover` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class DocumentDiscoverDict(TypedDict, total=False):
    url: Required[str]
