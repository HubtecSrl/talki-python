from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.range_unit import RangeUnit
from ..models.service_booking_mode import ServiceBookingMode

T = TypeVar("T", bound="Service")


@_attrs_define
class Service:
    """One bookable thing the business offers. Capacity is published on `Resource`, not here; `Resource.services` links the
    two. Inactive services stay in the feed: filter on `is_active` for a snapshot, never while syncing. A deleted
    service leaves the feed; `service.deleted` announces it, with the service as it was. Without the events, reconcile
    deletions with a full walk from no cursor.

        Attributes:
            id (str): Opaque Talki service identifier.
            location_id (str): The location that offers it (`GET /v1/locations`). Each location has services of its own, so
                two locations selling the same thing have one service each, with its own id, price and availability. Never null,
                and it never changes.
            name (str): What the business calls this service.
            description (None | str): Longer description shown to a customer, or null.
            price (None | str): Price as the owner wrote it: free text, not a number, such as "25€", "from 25€" or "price on
                request", usually in Italian. Do not parse it into a currency amount; render it as-is. Null when no price is
                published.
            duration_minutes (int | None): How long one booking of this service lasts, in minutes. Null when `booking_mode`
                is `day_range` — a stay is measured in nights or days, not minutes — and null for a service with no fixed
                length.
            booking_mode (ServiceBookingMode): `duration` for a timed slot (the common case), or `day_range` for a stay
                spanning whole nights or days: a hotel room, a multi-day rental. Read this before `duration_minutes`; the two
                modes are booked with different information.
            range_unit (None | RangeUnit): `nights` (check-out day is free again) or `days` (the whole last day is held).
                Only set when `booking_mode` is `day_range`, null otherwise.
            min_stay (int | None): Shortest stay accepted, in `range_unit` units. Null = no floor.
            max_stay (int | None): Longest stay accepted, in `range_unit` units. Null = no cap.
            checkin_time (None | str): Local check-in time as `HH:MM`, for a `day_range` service. Wall-clock time in the
                account's timezone (`GET /v1/account`), not UTC and not an instant: it is the same on every date, across
                daylight-saving changes.
            checkout_time (None | str): Local check-out time as `HH:MM`. Same rules as `checkin_time`.
            asks_quantity (bool): True when a booking of this service carries a count — covers, people, items — and the
                assistant asks for it. False when one booking always means one unit.
            quantity_label (None | str): What that count is called, in the business's own words and language (for example
                "people" or "covers", usually in Italian). Null when `asks_quantity` is false, or when the owner left it
                unnamed.
            min_quantity (int): Smallest count a booking may carry.
            max_quantity (int | None): Largest count a booking may carry. Null = no per-booking cap.
            is_active (bool): False when the business has switched the service off. It is still published — see the note on
                this object — but it is not bookable and should not be offered.
            created_at (datetime.datetime): When the service was added, RFC 3339 UTC.
            updated_at (datetime.datetime): Last change to the service, RFC 3339 UTC. Show it to a human; **do not sync on
                it**, for the reason given on `Appointment.updated_at`.
    """

    id: str
    location_id: str
    name: str
    description: None | str
    price: None | str
    duration_minutes: int | None
    booking_mode: ServiceBookingMode
    range_unit: None | RangeUnit
    min_stay: int | None
    max_stay: int | None
    checkin_time: None | str
    checkout_time: None | str
    asks_quantity: bool
    quantity_label: None | str
    min_quantity: int
    max_quantity: int | None
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        name = self.name

        description: None | str
        description = self.description

        price: None | str
        price = self.price

        duration_minutes: int | None
        duration_minutes = self.duration_minutes

        booking_mode = self.booking_mode.value

        range_unit: None | str
        if isinstance(self.range_unit, RangeUnit):
            range_unit = self.range_unit.value
        else:
            range_unit = self.range_unit

        min_stay: int | None
        min_stay = self.min_stay

        max_stay: int | None
        max_stay = self.max_stay

        checkin_time: None | str
        checkin_time = self.checkin_time

        checkout_time: None | str
        checkout_time = self.checkout_time

        asks_quantity = self.asks_quantity

        quantity_label: None | str
        quantity_label = self.quantity_label

        min_quantity = self.min_quantity

        max_quantity: int | None
        max_quantity = self.max_quantity

        is_active = self.is_active

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "name": name,
                "description": description,
                "price": price,
                "duration_minutes": duration_minutes,
                "booking_mode": booking_mode,
                "range_unit": range_unit,
                "min_stay": min_stay,
                "max_stay": max_stay,
                "checkin_time": checkin_time,
                "checkout_time": checkout_time,
                "asks_quantity": asks_quantity,
                "quantity_label": quantity_label,
                "min_quantity": min_quantity,
                "max_quantity": max_quantity,
                "is_active": is_active,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("location_id")

        name = d.pop("name")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        def _parse_price(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        price = _parse_price(d.pop("price"))

        def _parse_duration_minutes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        duration_minutes = _parse_duration_minutes(d.pop("duration_minutes"))

        booking_mode = ServiceBookingMode(d.pop("booking_mode"))

        def _parse_range_unit(data: object) -> None | RangeUnit:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                range_unit_type_0 = RangeUnit(data)

                return range_unit_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RangeUnit, data)

        range_unit = _parse_range_unit(d.pop("range_unit"))

        def _parse_min_stay(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        min_stay = _parse_min_stay(d.pop("min_stay"))

        def _parse_max_stay(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_stay = _parse_max_stay(d.pop("max_stay"))

        def _parse_checkin_time(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        checkin_time = _parse_checkin_time(d.pop("checkin_time"))

        def _parse_checkout_time(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        checkout_time = _parse_checkout_time(d.pop("checkout_time"))

        asks_quantity = d.pop("asks_quantity")

        def _parse_quantity_label(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        quantity_label = _parse_quantity_label(d.pop("quantity_label"))

        min_quantity = d.pop("min_quantity")

        def _parse_max_quantity(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        max_quantity = _parse_max_quantity(d.pop("max_quantity"))

        is_active = d.pop("is_active")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        service = cls(
            id=id,
            location_id=location_id,
            name=name,
            description=description,
            price=price,
            duration_minutes=duration_minutes,
            booking_mode=booking_mode,
            range_unit=range_unit,
            min_stay=min_stay,
            max_stay=max_stay,
            checkin_time=checkin_time,
            checkout_time=checkout_time,
            asks_quantity=asks_quantity,
            quantity_label=quantity_label,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at,
        )

        service.additional_properties = d
        return service

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
