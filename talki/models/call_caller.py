from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CallCaller")


@_attrs_define
class CallCaller:
    """Who called, as far as the account knows. Always present; its fields may be null. `display_name` is set only for a
    name the owner entered or imported, never for one the assistant heard.

        Attributes:
            contact_id (None | str): Talki contact this number resolves to, or null if the account has no contact for it.
                Stable per (account, number).
            phone_number (None | str): Caller's number in E.164, or null when the CallerID was withheld.
            display_name (None | str): Contact name, only when the account owner entered it by hand or imported it from
                their own address book. Null otherwise, including when the only name available was heard on the call.
    """

    contact_id: None | str
    phone_number: None | str
    display_name: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        contact_id: None | str
        contact_id = self.contact_id

        phone_number: None | str
        phone_number = self.phone_number

        display_name: None | str
        display_name = self.display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "contact_id": contact_id,
                "phone_number": phone_number,
                "display_name": display_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_contact_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        contact_id = _parse_contact_id(d.pop("contact_id"))

        def _parse_phone_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_number = _parse_phone_number(d.pop("phone_number"))

        def _parse_display_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        display_name = _parse_display_name(d.pop("display_name"))

        call_caller = cls(
            contact_id=contact_id,
            phone_number=phone_number,
            display_name=display_name,
        )

        call_caller.additional_properties = d
        return call_caller

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
