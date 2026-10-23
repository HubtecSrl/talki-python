from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UnresolvedRequestTeaching")


@_attrs_define
class UnresolvedRequestTeaching:
    """Where a taught answer went. The FAQ is indexed after the response, so the assistant uses the answer shortly after,
    not at once.

        Attributes:
            unresolved_request_id (str): The request it was taught from.
            location_id (None | str): The location whose FAQ it went into; null for every location.
            taught_at (datetime.datetime): When it was added, RFC 3339 UTC.
    """

    unresolved_request_id: str
    location_id: None | str
    taught_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        unresolved_request_id = self.unresolved_request_id

        location_id: None | str
        location_id = self.location_id

        taught_at = self.taught_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "unresolved_request_id": unresolved_request_id,
                "location_id": location_id,
                "taught_at": taught_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        unresolved_request_id = d.pop("unresolved_request_id")

        def _parse_location_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        location_id = _parse_location_id(d.pop("location_id"))

        taught_at = datetime.datetime.fromisoformat(d.pop("taught_at"))

        unresolved_request_teaching = cls(
            unresolved_request_id=unresolved_request_id,
            location_id=location_id,
            taught_at=taught_at,
        )

        unresolved_request_teaching.additional_properties = d
        return unresolved_request_teaching

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
