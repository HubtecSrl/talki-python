from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, TypedDict, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentSiteReplace")


@_attrs_define
class DocumentSiteReplace:
    """A website's new import, sent as `application/json`: the `pages` listed, or else the pages it holds.

    Attributes:
        pages (list[str] | None | Unset): The pages to read this time. Omit to read again the pages it holds (`GET
            /v1/documents/{document_id}/pages`).
    """

    pages: list[str] | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        pages: list[str] | None | Unset
        if isinstance(self.pages, Unset):
            pages = UNSET
        elif isinstance(self.pages, list):
            pages = self.pages

        else:
            pages = self.pages

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if pages is not UNSET:
            field_dict["pages"] = pages

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

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

        document_site_replace = cls(
            pages=pages,
        )

        return document_site_replace


# `DocumentSiteReplace` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class DocumentSiteReplaceDict(TypedDict, total=False):
    pages: Sequence[str] | None
