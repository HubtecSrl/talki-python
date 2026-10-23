from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.line_status import LineStatus

T = TypeVar("T", bound="LocationLine")


@_attrs_define
class LocationLine:
    """How a location's calls reach Talki: its own line forwards to its Talki number. For the main location, the same
    values as `Account.line`.

        Attributes:
            phone_number (None | str): The location's Talki number, E.164; the same as `Location.phone_number`.
            forwarding_number (None | str): The location's own line, which forwards its calls to `phone_number`, E.164. For
                the main location, the account's `forwarding_number`. Null when not set.
            status (LineStatus): Whether a line is proven to forward to Talki. `no_number` while there is no Talki number.
                `unverified` until a forwarding check of the current forwarding number has succeeded. `verified` once one has;
                it proves forwarding was on at `verified_at`, not that it still is.
            verified_at (datetime.datetime | None): When a forwarding check of the current `forwarding_number` last
                succeeded, RFC 3339 UTC. Null unless `status` is `verified`.
    """

    phone_number: None | str
    forwarding_number: None | str
    status: LineStatus
    verified_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        phone_number: None | str
        phone_number = self.phone_number

        forwarding_number: None | str
        forwarding_number = self.forwarding_number

        status = self.status.value

        verified_at: None | str
        if isinstance(self.verified_at, datetime.datetime):
            verified_at = self.verified_at.isoformat()
        else:
            verified_at = self.verified_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "phone_number": phone_number,
                "forwarding_number": forwarding_number,
                "status": status,
                "verified_at": verified_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_phone_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_number = _parse_phone_number(d.pop("phone_number"))

        def _parse_forwarding_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        forwarding_number = _parse_forwarding_number(d.pop("forwarding_number"))

        status = LineStatus(d.pop("status"))

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

        location_line = cls(
            phone_number=phone_number,
            forwarding_number=forwarding_number,
            status=status,
            verified_at=verified_at,
        )

        location_line.additional_properties = d
        return location_line

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
