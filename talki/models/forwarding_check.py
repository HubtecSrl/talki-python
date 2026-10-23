from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.forwarding_check_status import ForwardingCheckStatus

T = TypeVar("T", bound="ForwardingCheck")


@_attrs_define
class ForwardingCheck:
    """The latest forwarding check of one location's line, the main one unless `?location_id=` names another. Poll `GET
    /v1/forwarding_check` every few seconds after starting one, with the same `location_id`: `pending` turns into
    `verified` or `not_detected` within about a minute.

        Attributes:
            location_id (str): The location whose line is checked, an id from `GET /v1/locations`: the one the request named
                with `location_id`, or the main location when it named none.
            status (ForwardingCheckStatus): `pending` while the check call is ringing, at most about a minute. `verified`
                when the call came back through forwarding, `not_detected` when it did not. Either result is kept for ten
                minutes, then the status returns to `idle`.
            reason (None | str): When `status` is `verified`, the forwarding condition the carrier reported, such as
                `unconditional`, `user-busy`, `no-answer` or `unavailable`. Null otherwise, or when the carrier reported none.
            verified_at (datetime.datetime | None): When `status` is `verified`, when the call came back, RFC 3339 UTC. Null
                otherwise.
            last_verified_at (datetime.datetime | None): The most recent time any check succeeded, RFC 3339 UTC, kept after
                `status` returns to `idle`. Null if no check has ever succeeded.
    """

    location_id: str
    status: ForwardingCheckStatus
    reason: None | str
    verified_at: datetime.datetime | None
    last_verified_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        location_id = self.location_id

        status = self.status.value

        reason: None | str
        reason = self.reason

        verified_at: None | str
        if isinstance(self.verified_at, datetime.datetime):
            verified_at = self.verified_at.isoformat()
        else:
            verified_at = self.verified_at

        last_verified_at: None | str
        if isinstance(self.last_verified_at, datetime.datetime):
            last_verified_at = self.last_verified_at.isoformat()
        else:
            last_verified_at = self.last_verified_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "location_id": location_id,
                "status": status,
                "reason": reason,
                "verified_at": verified_at,
                "last_verified_at": last_verified_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        location_id = d.pop("location_id")

        status = ForwardingCheckStatus(d.pop("status"))

        def _parse_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        reason = _parse_reason(d.pop("reason"))

        def _parse_verified_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                verified_at_type_0 = datetime.datetime.fromisoformat(data)

                return verified_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        verified_at = _parse_verified_at(d.pop("verified_at"))

        def _parse_last_verified_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_verified_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_verified_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_verified_at = _parse_last_verified_at(d.pop("last_verified_at"))

        forwarding_check = cls(
            location_id=location_id,
            status=status,
            reason=reason,
            verified_at=verified_at,
            last_verified_at=last_verified_at,
        )

        forwarding_check.additional_properties = d
        return forwarding_check

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
