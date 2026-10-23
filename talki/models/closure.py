from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.closure_kind import ClosureKind

T = TypeVar("T", bound="Closure")


@_attrs_define
class Closure:
    """A dated exception to `WorkingHours`: a closure (`kind: closed`), when the business takes no bookings, or a special
    opening (`kind: open`), extra hours on one day that are added to that day's weekly hours. It applies at one
    location, or at every location when `location_id` is null. Appointments already inside a closure are not cancelled:
    look them up with `GET /v1/appointments` and `starts_after`/`starts_before`.

        Attributes:
            id (str): Closure identifier.
            location_id (None | str): The one location it applies at (`GET /v1/locations`), or null when it applies at every
                location of the account. Set when it is created, and never changed.
            kind (ClosureKind): `closed` for a closure, `open` for a special opening.
            all_day (bool): True for whole days, given by `start_date` and `end_date`; only a closure can be whole days.
                False for an exact range, given by `start_at` and `end_at`.
            start_date (None | str): First day, `YYYY-MM-DD`, when `all_day` is true. Null otherwise.
            end_date (None | str): Last day, included, `YYYY-MM-DD`, when `all_day` is true. Null otherwise.
            start_at (datetime.datetime): Start, RFC 3339 UTC. For whole days this is midnight at the start of `start_date`
                in the account's `timezone`.
            end_at (datetime.datetime): End, exclusive, RFC 3339 UTC. For whole days this is midnight at the end of
                `end_date`.
            reason (None | str): Why, such as "ferie estive". The assistant can tell callers. Null when none was given.
            created_at (datetime.datetime): When it was added, RFC 3339 UTC.
    """

    id: str
    location_id: None | str
    kind: ClosureKind
    all_day: bool
    start_date: None | str
    end_date: None | str
    start_at: datetime.datetime
    end_at: datetime.datetime
    reason: None | str
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id: None | str
        location_id = self.location_id

        kind = self.kind.value

        all_day = self.all_day

        start_date: None | str
        start_date = self.start_date

        end_date: None | str
        end_date = self.end_date

        start_at = self.start_at.isoformat()

        end_at = self.end_at.isoformat()

        reason: None | str
        reason = self.reason

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "kind": kind,
                "all_day": all_day,
                "start_date": start_date,
                "end_date": end_date,
                "start_at": start_at,
                "end_at": end_at,
                "reason": reason,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_location_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        location_id = _parse_location_id(d.pop("location_id"))

        kind = ClosureKind(d.pop("kind"))

        all_day = d.pop("all_day")

        def _parse_start_date(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        start_date = _parse_start_date(d.pop("start_date"))

        def _parse_end_date(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        end_date = _parse_end_date(d.pop("end_date"))

        start_at = datetime.datetime.fromisoformat(d.pop("start_at"))

        end_at = datetime.datetime.fromisoformat(d.pop("end_at"))

        def _parse_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        reason = _parse_reason(d.pop("reason"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        closure = cls(
            id=id,
            location_id=location_id,
            kind=kind,
            all_day=all_day,
            start_date=start_date,
            end_date=end_date,
            start_at=start_at,
            end_at=end_at,
            reason=reason,
            created_at=created_at,
        )

        closure.additional_properties = d
        return closure

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
