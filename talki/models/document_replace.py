from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Required, TypedDict, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentReplace")


@_attrs_define
class DocumentReplace:
    """A note's new text, sent as `application/json`.

    Attributes:
        body (str): Its new text, at most 100 KB in UTF-8.
        title (None | str | Unset): Its new title. Omit to keep the current one.
    """

    body: str
    title: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        body = self.body

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "body": body,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        body = d.pop("body")

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        document_replace = cls(
            body=body,
            title=title,
        )

        return document_replace


# `DocumentReplace` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class DocumentReplaceDict(TypedDict, total=False):
    body: Required[str]
    title: str | None
