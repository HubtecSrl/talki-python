from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AvailabilityInterval")


@_attrs_define
class AvailabilityInterval:
    """A window a booking fits in, not a slot. For a `duration` service a booking may start anywhere from `start_at` to
    `end_at` minus the service's `duration_minutes`; there is no start grid. For a `day_range` service the window is the
    stay you asked about: check-in to check-out, present only when that exact stay can be booked.

        Attributes:
            start_at (datetime.datetime): Start of the bookable window, RFC 3339 UTC.
            end_at (datetime.datetime): End of the bookable window, RFC 3339 UTC.
    """

    start_at: datetime.datetime
    end_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_at = self.start_at.isoformat()

        end_at = self.end_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_at": start_at,
                "end_at": end_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_at = datetime.datetime.fromisoformat(d.pop("start_at"))

        end_at = datetime.datetime.fromisoformat(d.pop("end_at"))

        availability_interval = cls(
            start_at=start_at,
            end_at=end_at,
        )

        availability_interval.additional_properties = d
        return availability_interval

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
