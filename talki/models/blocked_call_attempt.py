from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BlockedCallAttempt")


@_attrs_define
class BlockedCallAttempt:
    """A call refused because its number is blocked. It has no `Call` record.

    Attributes:
        id (str): Identifier of the attempt.
        location_id (str): The location the call was for, whose rule refused it (`GET /v1/locations`). Never null.
        phone_number (None | str): The caller's number, E.164.
        label (None | str): The label of the rule that blocked it, or null once that rule is deleted.
        attempted_at (datetime.datetime): When the call came in, RFC 3339 UTC.
    """

    id: str
    location_id: str
    phone_number: None | str
    label: None | str
    attempted_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        phone_number: None | str
        phone_number = self.phone_number

        label: None | str
        label = self.label

        attempted_at = self.attempted_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "phone_number": phone_number,
                "label": label,
                "attempted_at": attempted_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("location_id")

        def _parse_phone_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_number = _parse_phone_number(d.pop("phone_number"))

        def _parse_label(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        label = _parse_label(d.pop("label"))

        attempted_at = datetime.datetime.fromisoformat(d.pop("attempted_at"))

        blocked_call_attempt = cls(
            id=id,
            location_id=location_id,
            phone_number=phone_number,
            label=label,
            attempted_at=attempted_at,
        )

        blocked_call_attempt.additional_properties = d
        return blocked_call_attempt

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
