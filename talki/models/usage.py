from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Usage")


@_attrs_define
class Usage:
    """Talk time used in the current period and what is left, in seconds. To show minutes, round `remaining_seconds` down.

    Attributes:
        unlimited (bool): True when the plan sets no limit on talk time. The allowance fields are then null.
        used_seconds (int): Talk time used in the current period.
        included_seconds (int | None): Talk time the plan includes per period. Null when `unlimited`.
        extra_seconds (int): Bought extra talk time left right now. It is spent only once `included_seconds` is used up,
            and what is left carries over to the next period while the subscription is active.
        allowance_seconds (int | None): Everything the current period may spend: the time the plan includes plus every
            bought second not spent in an earlier period. Null when `unlimited`.
        remaining_seconds (int | None): `allowance_seconds` less `used_seconds`, never negative. Calls are refused when
            it reaches 0. Null when `unlimited`. To show it in minutes, round down, so no minute is shown that cannot be
            spent.
        period_start (None | str): When the current period began, RFC 3339 UTC.
        resets_at (datetime.datetime | None): When `used_seconds` returns to 0 and the plan's time is available again,
            RFC 3339 UTC. Null when nothing will renew it, such as a subscription that has ended.
    """

    unlimited: bool
    used_seconds: int
    included_seconds: int | None
    extra_seconds: int
    allowance_seconds: int | None
    remaining_seconds: int | None
    period_start: None | str
    resets_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        unlimited = self.unlimited

        used_seconds = self.used_seconds

        included_seconds: int | None
        included_seconds = self.included_seconds

        extra_seconds = self.extra_seconds

        allowance_seconds: int | None
        allowance_seconds = self.allowance_seconds

        remaining_seconds: int | None
        remaining_seconds = self.remaining_seconds

        period_start: None | str
        period_start = self.period_start

        resets_at: None | str
        if isinstance(self.resets_at, datetime.datetime):
            resets_at = self.resets_at.isoformat()
        else:
            resets_at = self.resets_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "unlimited": unlimited,
                "used_seconds": used_seconds,
                "included_seconds": included_seconds,
                "extra_seconds": extra_seconds,
                "allowance_seconds": allowance_seconds,
                "remaining_seconds": remaining_seconds,
                "period_start": period_start,
                "resets_at": resets_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        unlimited = d.pop("unlimited")

        used_seconds = d.pop("used_seconds")

        def _parse_included_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        included_seconds = _parse_included_seconds(d.pop("included_seconds"))

        extra_seconds = d.pop("extra_seconds")

        def _parse_allowance_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        allowance_seconds = _parse_allowance_seconds(d.pop("allowance_seconds"))

        def _parse_remaining_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        remaining_seconds = _parse_remaining_seconds(d.pop("remaining_seconds"))

        def _parse_period_start(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        period_start = _parse_period_start(d.pop("period_start"))

        def _parse_resets_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resets_at_type_0 = datetime.datetime.fromisoformat(data)

                return resets_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        resets_at = _parse_resets_at(d.pop("resets_at"))

        usage = cls(
            unlimited=unlimited,
            used_seconds=used_seconds,
            included_seconds=included_seconds,
            extra_seconds=extra_seconds,
            allowance_seconds=allowance_seconds,
            remaining_seconds=remaining_seconds,
            period_start=period_start,
            resets_at=resets_at,
        )

        usage.additional_properties = d
        return usage

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
