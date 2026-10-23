from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.location_status import LocationStatus

if TYPE_CHECKING:
    from ..models.location_line import LocationLine


T = TypeVar("T", bound="Location")


@_attrs_define
class Location:
    """One place the business works from, with its own Talki number, assistant settings, weekly hours, line, services,
    resources and bookings. Every account has exactly one main location (`is_default`). Locations are created, renamed
    and switched off in Talki only; an inactive one stays listed with its records, takes no calls or bookings and has no
    Talki number.

        Attributes:
            id (str): Opaque Talki location identifier.
            name (str): What the business calls the location; what the assistant names it to callers. Unique among active
                locations, not among all of them: key on `id`.
            is_default (bool): True for the main location, exactly one per account. It is never switched off.
            status (LocationStatus): `active` — it answers its calls and takes bookings. `inactive` — switched off in Talki,
                by the owner or because the plan has room for fewer locations: its records stay, it takes no calls or bookings,
                and it has no Talki number.
            phone_number (None | str): The Talki number that answers this location's calls, E.164. For the main location,
                the account's `phone_number`. Null while inactive, and while none is assigned.
            line (LocationLine): How a location's calls reach Talki: its own line forwards to its Talki number. For the main
                location, the same values as `Account.line`.
            position (int): The owner's display order, lowest first. Not unique.
            created_at (datetime.datetime): When the location was added, RFC 3339 UTC.
            deactivated_at (datetime.datetime | None): When it was last switched off, RFC 3339 UTC. Null while active.
    """

    id: str
    name: str
    is_default: bool
    status: LocationStatus
    phone_number: None | str
    line: LocationLine
    position: int
    created_at: datetime.datetime
    deactivated_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        is_default = self.is_default

        status = self.status.value

        phone_number: None | str
        phone_number = self.phone_number

        line = self.line.to_dict()

        position = self.position

        created_at = self.created_at.isoformat()

        deactivated_at: None | str
        if isinstance(self.deactivated_at, datetime.datetime):
            deactivated_at = self.deactivated_at.isoformat()
        else:
            deactivated_at = self.deactivated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "is_default": is_default,
                "status": status,
                "phone_number": phone_number,
                "line": line,
                "position": position,
                "created_at": created_at,
                "deactivated_at": deactivated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.location_line import LocationLine  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        is_default = d.pop("is_default")

        status = LocationStatus(d.pop("status"))

        def _parse_phone_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_number = _parse_phone_number(d.pop("phone_number"))

        line = LocationLine.from_dict(d.pop("line"))

        position = d.pop("position")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_deactivated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deactivated_at_type_0 = datetime.datetime.fromisoformat(data)

                return deactivated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        deactivated_at = _parse_deactivated_at(d.pop("deactivated_at"))

        location = cls(
            id=id,
            name=name,
            is_default=is_default,
            status=status,
            phone_number=phone_number,
            line=line,
            position=position,
            created_at=created_at,
            deactivated_at=deactivated_at,
        )

        location.additional_properties = d
        return location

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
