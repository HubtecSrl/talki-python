from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Literal, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.closure_kind import ClosureKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="ClosureUpdate")


@_attrs_define
class ClosureUpdate:
    """A partial edit of a closure or special opening. To move it, send the whole new window in one of the two forms. It
    stays at the location it was created for.

        Attributes:
            kind (ClosureKind | None | Unset): `closed` or `open`. Cannot be null. Turning a closure into a special opening
                needs a window that starts and ends on one day.
            all_day (bool | None | Unset): Whole days or an exact range. Cannot be null.
            start_date (None | str | Unset): First day, `YYYY-MM-DD`.
            end_date (None | str | Unset): Last day, included, `YYYY-MM-DD`.
            start_at (datetime.datetime | None | Unset): Start, RFC 3339 with a UTC offset.
            end_at (datetime.datetime | None | Unset): End, RFC 3339 with a UTC offset. Must be after `start_at`.
            reason (None | str | Unset): Replaces the reason. Send `null` or an empty string to remove it.
            location_id (None | str | Unset): Cannot be changed. Accepted only when it is the closure's own `location_id`
                (`null` for one of every location), so a client may send the whole object back; any other value is refused with
                `invalid_parameter`.
    """

    kind: ClosureKind | None | Unset = UNSET
    all_day: bool | None | Unset = UNSET
    start_date: None | str | Unset = UNSET
    end_date: None | str | Unset = UNSET
    start_at: datetime.datetime | None | Unset = UNSET
    end_at: datetime.datetime | None | Unset = UNSET
    reason: None | str | Unset = UNSET
    location_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind: None | str | Unset
        if isinstance(self.kind, Unset):
            kind = UNSET
        elif isinstance(self.kind, ClosureKind):
            kind = self.kind.value
        else:
            kind = self.kind

        all_day: bool | None | Unset
        if isinstance(self.all_day, Unset):
            all_day = UNSET
        else:
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

        def _parse_kind(data: object) -> ClosureKind | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                kind_type_0 = ClosureKind(data)

                return kind_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ClosureKind | None | Unset, data)

        kind = _parse_kind(d.pop("kind", UNSET))

        def _parse_all_day(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        all_day = _parse_all_day(d.pop("all_day", UNSET))

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

        closure_update = cls(
            kind=kind,
            all_day=all_day,
            start_date=start_date,
            end_date=end_date,
            start_at=start_at,
            end_at=end_at,
            reason=reason,
            location_id=location_id,
        )

        closure_update.additional_properties = d
        return closure_update

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


# `ClosureUpdate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class ClosureUpdateDict(TypedDict, total=False):
    kind: ClosureKind | Literal["closed", "open"] | None
    all_day: bool | None
    start_date: str | None
    end_date: str | None
    start_at: datetime.datetime | str | None
    end_at: datetime.datetime | str | None
    reason: str | None
    location_id: str | None
