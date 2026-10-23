from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContactUpsert")


@_attrs_define
class ContactUpsert:
    """Create or update the contact with this phone number: the number is the identity, and `external_id` is your cross-
    reference for finding it again after a number changes. A name written here is not overwritten by what the assistant
    hears on later calls. On a contact whose name was only guessed from a call, sending either name replaces both: the
    one you omit is cleared.

        Attributes:
            phone_number (str): The contact's number. E.164 preferred; an Italian national number is normalised. A number
                that cannot be parsed is rejected.
            first_name (None | str | Unset): Given name, or null.
            last_name (None | str | Unset): Family name, or null.
            notes (None | str | Unset): Customer-visible notes about this person, returned as `Contact.notes`.
            external_id (None | str | Unset): Your own id for this person. Stored as a cross-reference, unique per (account,
                system, id). Supply it and a later upsert finds the same contact even if the phone number changed.
            system (None | str | Unset): Which system `external_id` belongs to, e.g. your product's name. Required when
                `external_id` is given; ignored otherwise.
    """

    phone_number: str
    first_name: None | str | Unset = UNSET
    last_name: None | str | Unset = UNSET
    notes: None | str | Unset = UNSET
    external_id: None | str | Unset = UNSET
    system: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        phone_number = self.phone_number

        first_name: None | str | Unset
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        last_name: None | str | Unset
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        external_id: None | str | Unset
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        system: None | str | Unset
        if isinstance(self.system, Unset):
            system = UNSET
        else:
            system = self.system

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "phone_number": phone_number,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if notes is not UNSET:
            field_dict["notes"] = notes
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if system is not UNSET:
            field_dict["system"] = system

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phone_number = d.pop("phone_number")

        def _parse_first_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        first_name = _parse_first_name(d.pop("first_name", UNSET))

        def _parse_last_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_name = _parse_last_name(d.pop("last_name", UNSET))

        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))

        def _parse_external_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_system(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        system = _parse_system(d.pop("system", UNSET))

        contact_upsert = cls(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            notes=notes,
            external_id=external_id,
            system=system,
        )

        contact_upsert.additional_properties = d
        return contact_upsert

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
