from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CallStatsDay")


@_attrs_define
class CallStatsDay:
    """One day of the period's series.

    Attributes:
        date (str): A local calendar day in the account's `timezone`, `YYYY-MM-DD`.
        calls (int): Calls that started that day.
        duration_seconds (int): Their total talk time.
    """

    date: str
    calls: int
    duration_seconds: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        calls = self.calls

        duration_seconds = self.duration_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "calls": calls,
                "duration_seconds": duration_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        calls = d.pop("calls")

        duration_seconds = d.pop("duration_seconds")

        call_stats_day = cls(
            date=date,
            calls=calls,
            duration_seconds=duration_seconds,
        )

        call_stats_day.additional_properties = d
        return call_stats_day

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
