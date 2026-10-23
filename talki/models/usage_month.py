from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UsageMonth")


@_attrs_define
class UsageMonth:
    """Talk time billed in one calendar month, in the account's `timezone`.

    Attributes:
        month (str): The month, `YYYY-MM`, in the account's `timezone`.
        start (str): Local midnight on its 1st, RFC 3339 UTC.
        end (str): Local midnight on the next month's 1st, RFC 3339 UTC, excluded.
        used_seconds (int): Talk time billed for the calls answered in the month that are still in the call log: the sum
            of their `duration_seconds`. A deleted call is no longer counted, though its time stays billed. Zero for a month
            with no calls.
        calls (int): Calls answered in the month that billed time and are still in the call log.
    """

    month: str
    start: str
    end: str
    used_seconds: int
    calls: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        month = self.month

        start = self.start

        end = self.end

        used_seconds = self.used_seconds

        calls = self.calls

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "month": month,
                "start": start,
                "end": end,
                "used_seconds": used_seconds,
                "calls": calls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        month = d.pop("month")

        start = d.pop("start")

        end = d.pop("end")

        used_seconds = d.pop("used_seconds")

        calls = d.pop("calls")

        usage_month = cls(
            month=month,
            start=start,
            end=end,
            used_seconds=used_seconds,
            calls=calls,
        )

        usage_month.additional_properties = d
        return usage_month

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
