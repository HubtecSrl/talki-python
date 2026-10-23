from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call_stats_caller import CallStatsCaller
    from ..models.call_stats_day import CallStatsDay


T = TypeVar("T", bound="CallStats")


@_attrs_define
class CallStats:
    """Call figures over a period (the last `days`, or the local days `from` to `to`), plus today, this week and this
    month, in the account's `timezone`.

        Attributes:
            period_days (int): How many days the period covers: `days`, or the days from `from` to `to`.
            period_start (str): Start of the period, RFC 3339 UTC, included.
            period_end (str): End of the period, RFC 3339 UTC, excluded: now, or local midnight after `to`.
            total_calls (int): Calls in the period.
            total_duration_seconds (int): Their total talk time, as billed (`Call.duration_seconds`).
            average_duration_seconds (float): Their average talk time, to one decimal. 0 with no calls.
            booked_calls (int): Calls in the period that booked at least one appointment, counted once however many they
                booked, and still counted if the booking was cancelled since.
            unresolved_calls (int): Calls in the period that left at least one question the assistant could not answer (`GET
                /v1/unresolved_requests`), counted once however many they left, whatever the requests' status now. A call may
                count here and in `booked_calls` both. Calls Talki refused are never in these figures: see `GET
                /v1/refused_calls/summary`.
            transferred_calls (int): Calls in the period the assistant transferred to a person, counted once however many
                transfers they had. Calls recorded before transfers were stored (see `Call.outcome`) are not counted, so a
                period reaching back before then undercounts.
            today (int): Calls since midnight today.
            this_week (int): Calls since Monday.
            this_month (int): Calls since the first of the month.
            daily (list[CallStatsDay]): One entry per day in the period that had calls, oldest first.
            top_callers (list[CallStatsCaller]): Up to ten numbers that called most in the period, most calls first.
    """

    period_days: int
    period_start: str
    period_end: str
    total_calls: int
    total_duration_seconds: int
    average_duration_seconds: float
    booked_calls: int
    unresolved_calls: int
    transferred_calls: int
    today: int
    this_week: int
    this_month: int
    daily: list[CallStatsDay]
    top_callers: list[CallStatsCaller]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period_days = self.period_days

        period_start = self.period_start

        period_end = self.period_end

        total_calls = self.total_calls

        total_duration_seconds = self.total_duration_seconds

        average_duration_seconds = self.average_duration_seconds

        booked_calls = self.booked_calls

        unresolved_calls = self.unresolved_calls

        transferred_calls = self.transferred_calls

        today = self.today

        this_week = self.this_week

        this_month = self.this_month

        daily = []
        for daily_item_data in self.daily:
            daily_item = daily_item_data.to_dict()
            daily.append(daily_item)

        top_callers = []
        for top_callers_item_data in self.top_callers:
            top_callers_item = top_callers_item_data.to_dict()
            top_callers.append(top_callers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period_days": period_days,
                "period_start": period_start,
                "period_end": period_end,
                "total_calls": total_calls,
                "total_duration_seconds": total_duration_seconds,
                "average_duration_seconds": average_duration_seconds,
                "booked_calls": booked_calls,
                "unresolved_calls": unresolved_calls,
                "transferred_calls": transferred_calls,
                "today": today,
                "this_week": this_week,
                "this_month": this_month,
                "daily": daily,
                "top_callers": top_callers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_stats_caller import CallStatsCaller  # noqa: PLC0415
        from ..models.call_stats_day import CallStatsDay  # noqa: PLC0415

        d = dict(src_dict)
        period_days = d.pop("period_days")

        period_start = d.pop("period_start")

        period_end = d.pop("period_end")

        total_calls = d.pop("total_calls")

        total_duration_seconds = d.pop("total_duration_seconds")

        average_duration_seconds = d.pop("average_duration_seconds")

        booked_calls = d.pop("booked_calls")

        unresolved_calls = d.pop("unresolved_calls")

        transferred_calls = d.pop("transferred_calls")

        today = d.pop("today")

        this_week = d.pop("this_week")

        this_month = d.pop("this_month")

        daily = []
        _daily = d.pop("daily")
        for daily_item_data in _daily:
            daily_item = CallStatsDay.from_dict(daily_item_data)

            daily.append(daily_item)

        top_callers = []
        _top_callers = d.pop("top_callers")
        for top_callers_item_data in _top_callers:
            top_callers_item = CallStatsCaller.from_dict(top_callers_item_data)

            top_callers.append(top_callers_item)

        call_stats = cls(
            period_days=period_days,
            period_start=period_start,
            period_end=period_end,
            total_calls=total_calls,
            total_duration_seconds=total_duration_seconds,
            average_duration_seconds=average_duration_seconds,
            booked_calls=booked_calls,
            unresolved_calls=unresolved_calls,
            transferred_calls=transferred_calls,
            today=today,
            this_week=this_week,
            this_month=this_month,
            daily=daily,
            top_callers=top_callers,
        )

        call_stats.additional_properties = d
        return call_stats

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
