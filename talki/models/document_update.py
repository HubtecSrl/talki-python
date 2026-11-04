from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypedDict, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentUpdate")


@_attrs_define
class DocumentUpdate:
    """A partial edit of a document: its title, or whether the assistant uses it.

    Attributes:
        title (str | Unset): Its new title. Not for a website, whose title is its address. A note's new title is indexed
            again, as a change of its text is.
        enabled (bool | Unset): Switch it off (`false`) or on again (`true`). Cannot be null.
    """

    title: str | Unset = UNSET
    enabled: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        enabled = self.enabled

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title", UNSET)

        enabled = d.pop("enabled", UNSET)

        document_update = cls(
            title=title,
            enabled=enabled,
        )

        return document_update


# `DocumentUpdate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class DocumentUpdateDict(TypedDict, total=False):
    title: str
    enabled: bool
