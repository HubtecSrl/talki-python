from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.availability_day import AvailabilityDay


T = TypeVar("T", bound="Availability")


@_attrs_define
class Availability:
    """When a service can be booked, over a range of days. Advisory, not a reservation: a window can be taken by a phone
    call a moment later, so a `409` from `POST /v1/appointments` after a clean lookup is normal. When the owner's Google
    or Outlook calendar is connected, their events are subtracted, so this can be narrower than what a booking would
    accept, never wider.

        Attributes:
            service_id (str): The service this availability is for.
            timezone (str): IANA timezone the `date` fields are in. The same value `GET /v1/account` publishes.
            duration_minutes (int | None): Length of one booking of this service, repeated here so a consumer can slice an
                interval into offers without a second request. Null for a `day_range` service, where the length came from your
                own `stay_length`.
            quantity (int): The party size this answer was computed for.
            days (list[AvailabilityDay]): One entry per local day in the requested range, in order.
    """

    service_id: str
    timezone: str
    duration_minutes: int | None
    quantity: int
    days: list[AvailabilityDay]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        timezone = self.timezone

        duration_minutes: int | None
        duration_minutes = self.duration_minutes

        quantity = self.quantity

        days = []
        for days_item_data in self.days:
            days_item = days_item_data.to_dict()
            days.append(days_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "timezone": timezone,
                "duration_minutes": duration_minutes,
                "quantity": quantity,
                "days": days,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.availability_day import AvailabilityDay  # noqa: PLC0415

        d = dict(src_dict)
        service_id = d.pop("service_id")

        timezone = d.pop("timezone")

        def _parse_duration_minutes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        duration_minutes = _parse_duration_minutes(d.pop("duration_minutes"))

        quantity = d.pop("quantity")

        days = []
        _days = d.pop("days")
        for days_item_data in _days:
            days_item = AvailabilityDay.from_dict(days_item_data)

            days.append(days_item)

        availability = cls(
            service_id=service_id,
            timezone=timezone,
            duration_minutes=duration_minutes,
            quantity=quantity,
            days=days,
        )

        availability.additional_properties = d
        return availability

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
