from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CallUpdate")


@_attrs_define
class CallUpdate:
    """Inbox state for one call. Send `read`, `archived` or both.

    Attributes:
        read (bool | None | Unset): `true` marks the call read, keeping the first `read_at`. `false` marks it unread,
            archived or not. Cannot be null.
        archived (bool | None | Unset): `true` archives the call and marks it read, whatever `read` says. `false`
            returns it to the inbox. Cannot be null.
    """

    read: bool | None | Unset = UNSET
    archived: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        read: bool | None | Unset
        if isinstance(self.read, Unset):
            read = UNSET
        else:
            read = self.read

        archived: bool | None | Unset
        if isinstance(self.archived, Unset):
            archived = UNSET
        else:
            archived = self.archived

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if read is not UNSET:
            field_dict["read"] = read
        if archived is not UNSET:
            field_dict["archived"] = archived

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_read(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        read = _parse_read(d.pop("read", UNSET))

        def _parse_archived(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        archived = _parse_archived(d.pop("archived", UNSET))

        call_update = cls(
            read=read,
            archived=archived,
        )

        call_update.additional_properties = d
        return call_update

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


# `CallUpdate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class CallUpdateDict(TypedDict, total=False):
    read: bool | None
    archived: bool | None
