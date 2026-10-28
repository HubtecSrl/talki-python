from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Required, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkingHoursSlot")


@_attrs_define
class WorkingHoursSlot:
    """One weekly opening: a time range, in the account's `timezone`, on one or more weekdays.

    Attributes:
        days (list[int]): Weekdays this range applies to, as ISO weekday numbers: 1 is Monday, 7 is Sunday.
        start (str): Opening time, `HH:MM` in the account's `timezone`.
        end (str): Closing time, `HH:MM` in the account's `timezone`. Must be after `start`: a range cannot cross
            midnight, so split one that does into two slots on consecutive days.
    """

    days: list[int]
    start: str
    end: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        days = self.days

        start = self.start

        end = self.end

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "days": days,
                "start": start,
                "end": end,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        days = cast(list[int], d.pop("days"))

        start = d.pop("start")

        end = d.pop("end")

        working_hours_slot = cls(
            days=days,
            start=start,
            end=end,
        )

        working_hours_slot.additional_properties = d
        return working_hours_slot

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


# `WorkingHoursSlot` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class WorkingHoursSlotDict(TypedDict, total=False):
    days: Required[Sequence[int]]
    start: Required[str]
    end: Required[str]
