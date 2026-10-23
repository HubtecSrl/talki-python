from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AppointmentClient")


@_attrs_define
class AppointmentClient:
    """Who the booking is for. Always present; `contact_id` and `phone_number` are null for a booking entered by hand. The
    name is the one the booking was taken under, exactly as the owner sees it, and may come from what the assistant
    heard on the call.

        Attributes:
            contact_id (None | str): Talki contact whose number is `phone_number`, when there is one. Null otherwise.
            name (str): First name the booking was taken under.
            surname (str): Surname the booking was taken under.
            phone_number (None | str): Client's number in E.164. Null when Talki has no number for the client, e.g. a caller
                who withheld theirs.
    """

    contact_id: None | str
    name: str
    surname: str
    phone_number: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        contact_id: None | str
        contact_id = self.contact_id

        name = self.name

        surname = self.surname

        phone_number: None | str
        phone_number = self.phone_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "contact_id": contact_id,
                "name": name,
                "surname": surname,
                "phone_number": phone_number,
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

        name = d.pop("name")

        surname = d.pop("surname")

        def _parse_phone_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_number = _parse_phone_number(d.pop("phone_number"))

        appointment_client = cls(
            contact_id=contact_id,
            name=name,
            surname=surname,
            phone_number=phone_number,
        )

        appointment_client.additional_properties = d
        return appointment_client

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
