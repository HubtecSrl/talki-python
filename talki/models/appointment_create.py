from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Required, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AppointmentCreate")


@_attrs_define
class AppointmentCreate:
    """A booking to create: one service per appointment, booked at that service's location. `notes` is visible to the
    business and stored on the booking.

        Attributes:
            client_name (str): First name the booking is taken under. Required.
            client_surname (str): Surname the booking is taken under. Required.
            start_at (datetime.datetime): Start of the booking, RFC 3339. Send UTC (`Z`) or an explicit offset; a timestamp
                without an offset is rejected.
            service_id (None | str | Unset): The service being booked, from `GET /v1/services`. Null books a generic slot
                with no service attached — accepted, but it consumes no service capacity and the assistant cannot describe it to
                a caller, so prefer a real service. The booking is made at the service's location (`Service.location_id`),
                against that location's hours, closures and resources; without a service, at the main location (`is_default` on
                `GET /v1/locations`). A service of an inactive location is refused with 400 `location_inactive`.
            client_phone_number (None | str | Unset): Client's number. E.164 preferred; an Italian national number is
                normalised. A number that cannot be parsed is rejected. Null to leave it empty.
            end_at (datetime.datetime | None | Unset): End of the booking, RFC 3339. Must be after `start_at`. For a service
                with a `duration_minutes`, omit it and Talki sets it from the duration; if sent, it must be exactly `start_at`
                plus the duration, or the booking is refused with 400 `invalid_parameter`. Required for a booking with no
                service. For a `day_range` service it is required and is the check-out moment — use the `end_at` of the window
                `GET /v1/availability` returned, which already carries the service's check-in and check-out times.
            quantity (int | Unset): Party size, for a service whose `asks_quantity` is true. For a service that does not
                ask, it is forced to 1 without an error. For a service that asks, it must lie within the service's
                `min_quantity`/`max_quantity` (`GET /v1/services`), or the booking is refused with 400 `invalid_parameter`.
                Omitted means 1, which a service with `min_quantity` of 2 or more refuses. Default: 1.
            notes (None | str | Unset): Customer-visible note on the booking, shown to the business alongside it. Null to
                leave it empty.
    """

    client_name: str
    client_surname: str
    start_at: datetime.datetime
    service_id: None | str | Unset = UNSET
    client_phone_number: None | str | Unset = UNSET
    end_at: datetime.datetime | None | Unset = UNSET
    quantity: int | Unset = 1
    notes: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_name = self.client_name

        client_surname = self.client_surname

        start_at = self.start_at.isoformat()

        service_id: None | str | Unset
        if isinstance(self.service_id, Unset):
            service_id = UNSET
        else:
            service_id = self.service_id

        client_phone_number: None | str | Unset
        if isinstance(self.client_phone_number, Unset):
            client_phone_number = UNSET
        else:
            client_phone_number = self.client_phone_number

        end_at: None | str | Unset
        if isinstance(self.end_at, Unset):
            end_at = UNSET
        elif isinstance(self.end_at, datetime.datetime):
            end_at = self.end_at.isoformat()
        else:
            end_at = self.end_at

        quantity = self.quantity

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_name": client_name,
                "client_surname": client_surname,
                "start_at": start_at,
            }
        )
        if service_id is not UNSET:
            field_dict["service_id"] = service_id
        if client_phone_number is not UNSET:
            field_dict["client_phone_number"] = client_phone_number
        if end_at is not UNSET:
            field_dict["end_at"] = end_at
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_name = d.pop("client_name")

        client_surname = d.pop("client_surname")

        start_at = datetime.datetime.fromisoformat(d.pop("start_at"))

        def _parse_service_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service_id = _parse_service_id(d.pop("service_id", UNSET))

        def _parse_client_phone_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        client_phone_number = _parse_client_phone_number(d.pop("client_phone_number", UNSET))

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

        quantity = d.pop("quantity", UNSET)

        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))

        appointment_create = cls(
            client_name=client_name,
            client_surname=client_surname,
            start_at=start_at,
            service_id=service_id,
            client_phone_number=client_phone_number,
            end_at=end_at,
            quantity=quantity,
            notes=notes,
        )

        appointment_create.additional_properties = d
        return appointment_create

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


# `AppointmentCreate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class AppointmentCreateDict(TypedDict, total=False):
    client_name: Required[str]
    client_surname: Required[str]
    start_at: Required[datetime.datetime | str]
    service_id: str | None
    client_phone_number: str | None
    end_at: datetime.datetime | str | None
    quantity: int
    notes: str | None
