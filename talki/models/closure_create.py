from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Literal, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.closure_kind import ClosureKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="ClosureCreate")


@_attrs_define
class ClosureCreate:
    """A new closure or special opening: `all_day: true` with `start_date` and `end_date` (closures only), or an exact
    range with `start_at` and `end_at`. Sending fields of both forms is refused, and so is a special opening that does
    not start and end on the same day in the account's `timezone`. Without `location_id`, it applies at every location.

        Attributes:
            kind (ClosureKind | Unset): `closed` for a closure, `open` for a special opening. Default: ClosureKind.CLOSED.
            all_day (bool | Unset): True to close whole days, given by `start_date` and `end_date`. False (the default) for
                an exact range, given by `start_at` and `end_at`. Only a closure can be whole days. Default: False.
            start_date (None | str | Unset): First closed day, `YYYY-MM-DD`. Required when `all_day` is true.
            end_date (None | str | Unset): Last closed day, included, `YYYY-MM-DD`. Required when `all_day` is true. The
                same as `start_date` for a single day.
            start_at (datetime.datetime | None | Unset): Start of the closure or special opening, RFC 3339 with a UTC
                offset. Required when `all_day` is false.
            end_at (datetime.datetime | None | Unset): End of the closure or special opening, exclusive, RFC 3339 with a UTC
                offset. Must be after `start_at`. Required when `all_day` is false. A special opening must end on the day it
                starts; midnight at the end of that day is allowed.
            reason (None | str | Unset): Why the business is closed, or open specially. The assistant can tell callers.
            location_id (None | str | Unset): The one location it applies at, an id from `GET /v1/locations` (inactive ones
                included). Omit it, or send `null`, for a closure or special opening of every location of the account. Cannot be
                changed afterwards.
    """

    kind: ClosureKind | Unset = ClosureKind.CLOSED
    all_day: bool | Unset = False
    start_date: None | str | Unset = UNSET
    end_date: None | str | Unset = UNSET
    start_at: datetime.datetime | None | Unset = UNSET
    end_at: datetime.datetime | None | Unset = UNSET
    reason: None | str | Unset = UNSET
    location_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        all_day = self.all_day

        start_date: None | str | Unset
        if isinstance(self.start_date, Unset):
            start_date = UNSET
        else:
            start_date = self.start_date

        end_date: None | str | Unset
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        else:
            end_date = self.end_date

        start_at: None | str | Unset
        if isinstance(self.start_at, Unset):
            start_at = UNSET
        elif isinstance(self.start_at, datetime.datetime):
            start_at = self.start_at.isoformat()
        else:
            start_at = self.start_at

        end_at: None | str | Unset
        if isinstance(self.end_at, Unset):
            end_at = UNSET
        elif isinstance(self.end_at, datetime.datetime):
            end_at = self.end_at.isoformat()
        else:
            end_at = self.end_at

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        location_id: None | str | Unset
        if isinstance(self.location_id, Unset):
            location_id = UNSET
        else:
            location_id = self.location_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if all_day is not UNSET:
            field_dict["all_day"] = all_day
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if start_at is not UNSET:
            field_dict["start_at"] = start_at
        if end_at is not UNSET:
            field_dict["end_at"] = end_at
        if reason is not UNSET:
            field_dict["reason"] = reason
        if location_id is not UNSET:
            field_dict["location_id"] = location_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _kind = d.pop("kind", UNSET)
        kind: ClosureKind | Unset
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = ClosureKind(_kind)

        all_day = d.pop("all_day", UNSET)

        def _parse_start_date(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        start_date = _parse_start_date(d.pop("start_date", UNSET))

        def _parse_end_date(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        end_date = _parse_end_date(d.pop("end_date", UNSET))

        def _parse_start_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_at_type_0 = datetime.datetime.fromisoformat(data)

                return start_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        start_at = _parse_start_at(d.pop("start_at", UNSET))

        def _parse_end_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_at_type_0 = datetime.datetime.fromisoformat(data)

                return end_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        end_at = _parse_end_at(d.pop("end_at", UNSET))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_location_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        location_id = _parse_location_id(d.pop("location_id", UNSET))

        closure_create = cls(
            kind=kind,
            all_day=all_day,
            start_date=start_date,
            end_date=end_date,
            start_at=start_at,
            end_at=end_at,
            reason=reason,
            location_id=location_id,
        )

        closure_create.additional_properties = d
        return closure_create

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


# `ClosureCreate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class ClosureCreateDict(TypedDict, total=False):
    kind: ClosureKind | Literal["closed", "open"]
    all_day: bool
    start_date: str | None
    end_date: str | None
    start_at: datetime.datetime | str | None
    end_at: datetime.datetime | str | None
    reason: str | None
    location_id: str | None
