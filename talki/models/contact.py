from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Contact")


@_attrs_define
class Contact:
    """A person in the account's address book. Only contacts the owner entered, imported or confirmed are published; names
    the assistant only heard are `PendingContact`s until the owner approves them. One contact per phone number; once
    stored, match on `id`.

        Attributes:
            id (str): Opaque Talki contact identifier.
            phone_number (str): The contact's number in E.164.
            first_name (None | str): Given name, or null.
            last_name (None | str): Family name, or null.
            display_name (None | str): First and last name joined, or null when both are absent.
            notes (None | str): Notes the account owner wrote about this person. Customer-visible text, never the
                assistant's own notes.
            last_call_at (datetime.datetime | None): Most recent call from this number, RFC 3339 UTC, or null.
            call_count (int | None): Calls received from this number, or null for an unverified contact returned by upsert.
            created_at (datetime.datetime): When the contact was added, RFC 3339 UTC.
            updated_at (datetime.datetime): Last change to the contact, RFC 3339 UTC. Show it to a human as "last modified";
                **do not sync on it**: as with `Appointment.updated_at`, a watermark on it can skip a contact permanently.
                Resume with the change feed's `next_cursor`.
    """

    id: str
    phone_number: str
    first_name: None | str
    last_name: None | str
    display_name: None | str
    notes: None | str
    last_call_at: datetime.datetime | None
    call_count: int | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        phone_number = self.phone_number

        first_name: None | str
        first_name = self.first_name

        last_name: None | str
        last_name = self.last_name

        display_name: None | str
        display_name = self.display_name

        notes: None | str
        notes = self.notes

        last_call_at: None | str
        if isinstance(self.last_call_at, datetime.datetime):
            last_call_at = self.last_call_at.isoformat()
        else:
            last_call_at = self.last_call_at

        call_count: int | None
        call_count = self.call_count

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
                "display_name": display_name,
                "notes": notes,
                "last_call_at": last_call_at,
                "call_count": call_count,
                "created_at": created_at,
                "updated_at": updated_at,
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

        def _parse_display_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        display_name = _parse_display_name(d.pop("display_name"))

        def _parse_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        notes = _parse_notes(d.pop("notes"))

        def _parse_last_call_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_call_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_call_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_call_at = _parse_last_call_at(d.pop("last_call_at"))

        def _parse_call_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        call_count = _parse_call_count(d.pop("call_count"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        contact = cls(
            id=id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            notes=notes,
            last_call_at=last_call_at,
            call_count=call_count,
            created_at=created_at,
            updated_at=updated_at,
        )

        contact.additional_properties = d
        return contact

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
