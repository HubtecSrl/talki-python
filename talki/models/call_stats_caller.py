from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CallStatsCaller")


@_attrs_define
class CallStatsCaller:
    """One of the numbers that called most in the period.

    Attributes:
        phone_number (str): The caller's number, E.164. A bare `+` stands for every caller who withheld their number.
        calls (int): Calls from this number in the period.
        duration_seconds (int): Their total talk time.
        last_call_at (datetime.datetime): When the latest of them started, RFC 3339 UTC.
    """

    phone_number: str
    calls: int
    duration_seconds: int
    last_call_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        phone_number = self.phone_number

        calls = self.calls

        duration_seconds = self.duration_seconds

        last_call_at = self.last_call_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "phone_number": phone_number,
                "calls": calls,
                "duration_seconds": duration_seconds,
                "last_call_at": last_call_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phone_number = d.pop("phone_number")

        calls = d.pop("calls")

        duration_seconds = d.pop("duration_seconds")

        last_call_at = datetime.datetime.fromisoformat(d.pop("last_call_at"))

        call_stats_caller = cls(
            phone_number=phone_number,
            calls=calls,
            duration_seconds=duration_seconds,
            last_call_at=last_call_at,
        )

        call_stats_caller.additional_properties = d
        return call_stats_caller

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
