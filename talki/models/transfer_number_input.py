from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Required, TypedDict, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TransferNumberInput")


@_attrs_define
class TransferNumberInput:
    """A transfer target to store; the number is stored as E.164.

    Attributes:
        label (str): Who answers at this number, such as "Reception". Unique within the list, ignoring case: the
            assistant picks a target by its label.
        phone (str): The number. E.164, or a national number, which is read in the country of the account's
            `phone_number`. Stored as E.164.
    """

    label: str
    phone: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        phone = self.phone

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "phone": phone,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        phone = d.pop("phone")

        transfer_number_input = cls(
            label=label,
            phone=phone,
        )

        transfer_number_input.additional_properties = d
        return transfer_number_input

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


# `TransferNumberInput` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class TransferNumberInputDict(TypedDict, total=False):
    label: Required[str]
    phone: Required[str]
