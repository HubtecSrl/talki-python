from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PendingContact")


@_attrs_define
class PendingContact:
    """A name the assistant heard on a call, waiting for the owner. It is not a contact and must not be stored as one:
    approve it to make it a contact, or discard it.

        Attributes:
            id (str): Identifier of the candidate.
            phone_number (str): The caller's number, E.164. A bare `+` stands for every caller who withheld their number.
            first_name (None | str): The given name heard, or null.
            last_name (None | str): The family name heard, or null.
            call_id (None | str): The call it was heard on, or null once that call has aged out.
            created_at (datetime.datetime): When it was first heard, RFC 3339 UTC.
    """

    id: str
    phone_number: str
    first_name: None | str
    last_name: None | str
    call_id: None | str
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        phone_number = self.phone_number

        first_name: None | str
        first_name = self.first_name

        last_name: None | str
        last_name = self.last_name

        call_id: None | str
        call_id = self.call_id

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
                "call_id": call_id,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        phone_number = d.pop("phone_number")

        def _parse_first_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        first_name = _parse_first_name(d.pop("first_name"))

        def _parse_last_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_name = _parse_last_name(d.pop("last_name"))

        def _parse_call_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        call_id = _parse_call_id(d.pop("call_id"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        pending_contact = cls(
            id=id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            call_id=call_id,
            created_at=created_at,
        )

        pending_contact.additional_properties = d
        return pending_contact

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
