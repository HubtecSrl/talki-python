from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.availability_interval import AvailabilityInterval


T = TypeVar("T", bound="AvailabilityDay")


@_attrs_define
class AvailabilityDay:
    """One local calendar day of the requested range. Every day is present, closed and fully booked ones included.

    Attributes:
        date (str): The local calendar date in the account's timezone, `YYYY-MM-DD`, not a UTC date. An interval shortly
            after local midnight starts on the previous UTC date.
        intervals (list[AvailabilityInterval]): Bookable windows on this day, earliest first. Empty when none.
        closed (bool): True when the business is shut for the whole day — a weekday with no working hours, or a closure
            the owner entered. Distinct from an open day that happens to be fully booked, where this is false and
            `intervals` is empty.
    """

    date: str
    intervals: list[AvailabilityInterval]
    closed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        intervals = []
        for intervals_item_data in self.intervals:
            intervals_item = intervals_item_data.to_dict()
            intervals.append(intervals_item)

        closed = self.closed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "intervals": intervals,
                "closed": closed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.availability_interval import AvailabilityInterval  # noqa: PLC0415

        d = dict(src_dict)
        date = d.pop("date")

        intervals = []
        _intervals = d.pop("intervals")
        for intervals_item_data in _intervals:
            intervals_item = AvailabilityInterval.from_dict(intervals_item_data)

            intervals.append(intervals_item)

        closed = d.pop("closed")

        availability_day = cls(
            date=date,
            intervals=intervals,
            closed=closed,
        )

        availability_day.additional_properties = d
        return availability_day

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
