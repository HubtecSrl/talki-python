from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Required, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WhatsAppScheduleRange")


@_attrs_define
class WhatsAppScheduleRange:
    """One time range of the `scheduled` mode, in Rome time.

    Attributes:
        days (list[int]): Weekdays the range applies to, as ISO weekday numbers: 1 is Monday, 7 is Sunday.
        start (str): Start, `HH:MM`, Rome time.
        end (str): End, `HH:MM`, Rome time, after `start`. `23:59` runs to midnight: a night is two ranges,
            `18:00`-`23:59` and `00:00`-`09:00` of the next day.
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

        whats_app_schedule_range = cls(
            days=days,
            start=start,
            end=end,
        )

        whats_app_schedule_range.additional_properties = d
        return whats_app_schedule_range

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


# `WhatsAppScheduleRange` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class WhatsAppScheduleRangeDict(TypedDict, total=False):
    days: Required[Sequence[int]]
    start: Required[str]
    end: Required[str]
