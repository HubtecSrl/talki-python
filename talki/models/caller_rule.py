from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.caller_rule_kind import CallerRuleKind

T = TypeVar("T", bound="CallerRule")


@_attrs_define
class CallerRule:
    """A VIP or blocked number of one location. A number is on one list at most at a location, so adding it to the other
    list moves it.

        Attributes:
            id (str): Rule identifier.
            location_id (str): The location whose calls it matches (`GET /v1/locations`). Never null, and it never changes.
            phone_number (str): The number, E.164.
            kind (CallerRuleKind): `vip` or `blocked`. A number is on one list at most at a location.
            label (None | str): The owner's name for it, or null.
            created_at (datetime.datetime): RFC 3339 UTC.
            updated_at (datetime.datetime): RFC 3339 UTC.
    """

    id: str
    location_id: str
    phone_number: str
    kind: CallerRuleKind
    label: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        phone_number = self.phone_number

        kind = self.kind.value

        label: None | str
        label = self.label

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "phone_number": phone_number,
                "kind": kind,
                "label": label,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("location_id")

        phone_number = d.pop("phone_number")

        kind = CallerRuleKind(d.pop("kind"))

        def _parse_label(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        label = _parse_label(d.pop("label"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        caller_rule = cls(
            id=id,
            location_id=location_id,
            phone_number=phone_number,
            kind=kind,
            label=label,
            created_at=created_at,
            updated_at=updated_at,
        )

        caller_rule.additional_properties = d
        return caller_rule

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
