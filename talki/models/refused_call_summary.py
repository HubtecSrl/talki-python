from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.refused_call_summary_by_reason import RefusedCallSummaryByReason


T = TypeVar("T", bound="RefusedCallSummary")


@_attrs_define
class RefusedCallSummary:
    """Refused calls over a period (the last `days`, or the local days `from` to `to`), by reason.

    Attributes:
        period_days (int): How many days the period covers: `days`, or the days from `from` to `to`.
        period_start (str): Start of the period, RFC 3339 UTC, included.
        period_end (str): End of the period, RFC 3339 UTC, excluded: now, or local midnight after `to`.
        total (int): Refused calls in the period.
        by_reason (RefusedCallSummaryByReason): Refused calls in the period per `reason` (the values listed on
            `RefusedCall.reason`). Reasons with none are omitted.
        recent (int): Refused calls in the last `recent_days` days.
        recent_days (int): The window `recent` counts, in days.
        actions (list[str]): Every `action` the period's refusals call for, sorted, without duplicates (the values
            listed on `RefusedCall.action`).
    """

    period_days: int
    period_start: str
    period_end: str
    total: int
    by_reason: RefusedCallSummaryByReason
    recent: int
    recent_days: int
    actions: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period_days = self.period_days

        period_start = self.period_start

        period_end = self.period_end

        total = self.total

        by_reason = self.by_reason.to_dict()

        recent = self.recent

        recent_days = self.recent_days

        actions = self.actions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period_days": period_days,
                "period_start": period_start,
                "period_end": period_end,
                "total": total,
                "by_reason": by_reason,
                "recent": recent,
                "recent_days": recent_days,
                "actions": actions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.refused_call_summary_by_reason import RefusedCallSummaryByReason  # noqa: PLC0415

        d = dict(src_dict)
        period_days = d.pop("period_days")

        period_start = d.pop("period_start")

        period_end = d.pop("period_end")

        total = d.pop("total")

        by_reason = RefusedCallSummaryByReason.from_dict(d.pop("by_reason"))

        recent = d.pop("recent")

        recent_days = d.pop("recent_days")

        actions = cast(list[str], d.pop("actions"))

        refused_call_summary = cls(
            period_days=period_days,
            period_start=period_start,
            period_end=period_end,
            total=total,
            by_reason=by_reason,
            recent=recent,
            recent_days=recent_days,
            actions=actions,
        )

        refused_call_summary.additional_properties = d
        return refused_call_summary

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
