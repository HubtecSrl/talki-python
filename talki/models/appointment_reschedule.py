from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AppointmentReschedule")


@_attrs_define
class AppointmentReschedule:
    """A partial edit of a booking. Every field is optional, and an omitted field is left unchanged, not cleared. A move
    that does not fit is refused with a conflict code; nothing is booked. A booking never changes location.

        Attributes:
            client_name (None | str | Unset): New first name, or null to leave it unchanged.
            client_surname (None | str | Unset): New surname, or null to leave it unchanged.
            client_phone_number (None | str | Unset): New client number, E.164 preferred, or null to leave it unchanged. A
                number that cannot be parsed is rejected.
            start_at (datetime.datetime | None | Unset): New start, RFC 3339 with an offset. Null leaves it unchanged.
            end_at (datetime.datetime | None | Unset): New end, RFC 3339 with an offset. Null leaves it unchanged — moving
                only `start_at` does NOT shift the end to preserve the duration, it moves one edge. Send both to move a booking.
    """

    client_name: None | str | Unset = UNSET
    client_surname: None | str | Unset = UNSET
    client_phone_number: None | str | Unset = UNSET
    start_at: datetime.datetime | None | Unset = UNSET
    end_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_name: None | str | Unset
        if isinstance(self.client_name, Unset):
            client_name = UNSET
        else:
            client_name = self.client_name

        client_surname: None | str | Unset
        if isinstance(self.client_surname, Unset):
            client_surname = UNSET
        else:
            client_surname = self.client_surname

        client_phone_number: None | str | Unset
        if isinstance(self.client_phone_number, Unset):
            client_phone_number = UNSET
        else:
            client_phone_number = self.client_phone_number

        start_at: None | str | Unset
        if isinstance(self.start_at, Unset):
            start_at = UNSET
        elif isinstance(self.start_at, datetime.datetime):
            start_at = self.start_at.isoformat()
        else:
            start_at = self.start_at

        end_at: None | str | Unset
        if isinstance(self.end_at, Unset):
            end_at = UNSET
        elif isinstance(self.end_at, datetime.datetime):
            end_at = self.end_at.isoformat()
        else:
            end_at = self.end_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if client_name is not UNSET:
            field_dict["client_name"] = client_name
        if client_surname is not UNSET:
            field_dict["client_surname"] = client_surname
        if client_phone_number is not UNSET:
            field_dict["client_phone_number"] = client_phone_number
        if start_at is not UNSET:
            field_dict["start_at"] = start_at
        if end_at is not UNSET:
            field_dict["end_at"] = end_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_client_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        client_name = _parse_client_name(d.pop("client_name", UNSET))

        def _parse_client_surname(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        client_surname = _parse_client_surname(d.pop("client_surname", UNSET))

        def _parse_client_phone_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        client_phone_number = _parse_client_phone_number(d.pop("client_phone_number", UNSET))

        def _parse_start_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_at_type_0 = datetime.datetime.fromisoformat(data)

                return start_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        start_at = _parse_start_at(d.pop("start_at", UNSET))

        def _parse_end_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_at_type_0 = datetime.datetime.fromisoformat(data)

                return end_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        end_at = _parse_end_at(d.pop("end_at", UNSET))

        appointment_reschedule = cls(
            client_name=client_name,
            client_surname=client_surname,
            client_phone_number=client_phone_number,
            start_at=start_at,
            end_at=end_at,
        )

        appointment_reschedule.additional_properties = d
        return appointment_reschedule

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


# `AppointmentReschedule` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class AppointmentRescheduleDict(TypedDict, total=False):
    client_name: str | None
    client_surname: str | None
    client_phone_number: str | None
    start_at: datetime.datetime | str | None
    end_at: datetime.datetime | str | None
