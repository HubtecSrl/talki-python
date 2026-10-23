from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.usage_month import UsageMonth


T = TypeVar("T", bound="UsageHistory")


@_attrs_define
class UsageHistory:
    """Talk time per calendar month, oldest first, from the call log. A call counts in the month it was answered in. A
    month is not a billing period, and the meter of `GET /v1/usage` adds a call once it has ended, so the current month
    can differ from it, and a call running past midnight into a new month counts here in the earlier one. A month reads
    less than was billed when some of its calls were deleted, through `DELETE /v1/calls/{call_id}` or in the apps, or
    are before `retained_since`.

        Attributes:
            months (list[UsageMonth]): One entry per month asked for, oldest first.
            retained_since (str): Calls older than this, RFC 3339 UTC, have been deleted by Talki's retention, so a month
                before it reads less than was billed.
    """

    months: list[UsageMonth]
    retained_since: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        months = []
        for months_item_data in self.months:
            months_item = months_item_data.to_dict()
            months.append(months_item)

        retained_since = self.retained_since

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "months": months,
                "retained_since": retained_since,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_month import UsageMonth  # noqa: PLC0415

        d = dict(src_dict)
        months = []
        _months = d.pop("months")
        for months_item_data in _months:
            months_item = UsageMonth.from_dict(months_item_data)

            months.append(months_item)

        retained_since = d.pop("retained_since")

        usage_history = cls(
            months=months,
            retained_since=retained_since,
        )

        usage_history.additional_properties = d
        return usage_history

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
