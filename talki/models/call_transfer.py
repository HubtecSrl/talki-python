from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CallTransfer")


@_attrs_define
class CallTransfer:
    """A hand-over of the call to a person, in the order it happened.

    Attributes:
        target_label (str): The destination as the owner named it in Talki (e.g. `Reception`). Never the number behind
            it.
        at (None | str): When the call was handed over, RFC 3339.
    """

    target_label: str
    at: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_label = self.target_label

        at: None | str
        at = self.at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target_label": target_label,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_label = d.pop("target_label")

        def _parse_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        at = _parse_at(d.pop("at"))

        call_transfer = cls(
            target_label=target_label,
            at=at,
        )

        call_transfer.additional_properties = d
        return call_transfer

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
