from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.resource_mode import ResourceMode

if TYPE_CHECKING:
    from ..models.resource_service_link import ResourceServiceLink
    from ..models.resource_unit_class import ResourceUnitClass


T = TypeVar("T", bound="Resource")


@_attrs_define
class Resource:
    """Something finite the business books against: tables, rooms, chairs, seats. Its unit classes and service links are
    included, and a change to either moves this resource in the change feed and sends `resource.updated`. A deleted
    resource leaves the feed; `resource.deleted` announces it. `capacity` means different things in the two modes; read
    the field descriptions before using it.

        Attributes:
            id (str): Opaque Talki resource identifier.
            location_id (str): The location it is at (`GET /v1/locations`). Capacity is physical: only services of the same
                location draw on it. Never null, and it never changes.
            name (str): What the business calls this resource.
            mode (ResourceMode): `shared` — one fungible pool of `capacity` units (covers, seats, slots). `units` — a set of
                discrete sized units, described by `unit_classes`.
            capacity (int): In `shared` mode, the total units available at one time. In `units` mode this is the size of the
                LARGEST SINGLE unit, not a total — a resource with six four-tops reports 4. Use `max_party_size` for the
                question you probably mean.
            max_party_size (int): The largest single booking this resource can hold at one time, in its own units, before
                any service's `rate` is applied. Equals `capacity` in `shared` mode; in `units` mode it is derived from the
                classes and the combining rules, so six combinable four-tops report more than 4. A booking above this is refused
                with `party_too_large`.
            combine_across_classes (bool): True when a single booking may join units of DIFFERENT classes (a four-top plus a
                two-top for six). Per-class `combinable` still governs whether a class may be joined at all. Always false for a
                `shared` resource.
            unit_classes (list[ResourceUnitClass]): The discrete units this resource is made of. Always empty for a `shared`
                resource.
            services (list[ResourceServiceLink]): Which services draw on this resource, and at what rate. Empty means no
                service currently books against it, which makes it inert rather than unlimited.
            owner_service_id (None | str): Set when this resource exists only for one service and is created, renamed and
                deleted with it: a service given its own limit (`initial_capacity`) gets one. Cleared as soon as a second
                service links to it, at which point the resource is shared and independent. Null for the default resource and
                for a resource the business created itself. Use it to tell a real shared resource ('this salon has three
                chairs') from a per-service cap ('haircuts at a time').
            is_default (bool): True for a location's default resource: the shared limit new duration services of that
                location draw on unless they are given their own or other resources, such as the salon's chairs. At most one per
                location.
            created_at (datetime.datetime): RFC 3339 UTC.
            updated_at (datetime.datetime): RFC 3339 UTC. Moves when the resource, any of its unit classes, or any of its
                service links changes.
    """

    id: str
    location_id: str
    name: str
    mode: ResourceMode
    capacity: int
    max_party_size: int
    combine_across_classes: bool
    unit_classes: list[ResourceUnitClass]
    services: list[ResourceServiceLink]
    owner_service_id: None | str
    is_default: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        name = self.name

        mode = self.mode.value

        capacity = self.capacity

        max_party_size = self.max_party_size

        combine_across_classes = self.combine_across_classes

        unit_classes = []
        for unit_classes_item_data in self.unit_classes:
            unit_classes_item = unit_classes_item_data.to_dict()
            unit_classes.append(unit_classes_item)

        services = []
        for services_item_data in self.services:
            services_item = services_item_data.to_dict()
            services.append(services_item)

        owner_service_id: None | str
        owner_service_id = self.owner_service_id

        is_default = self.is_default

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "name": name,
                "mode": mode,
                "capacity": capacity,
                "max_party_size": max_party_size,
                "combine_across_classes": combine_across_classes,
                "unit_classes": unit_classes,
                "services": services,
                "owner_service_id": owner_service_id,
                "is_default": is_default,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_service_link import ResourceServiceLink  # noqa: PLC0415
        from ..models.resource_unit_class import ResourceUnitClass  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("location_id")

        name = d.pop("name")

        mode = ResourceMode(d.pop("mode"))

        capacity = d.pop("capacity")

        max_party_size = d.pop("max_party_size")

        combine_across_classes = d.pop("combine_across_classes")

        unit_classes = []
        _unit_classes = d.pop("unit_classes")
        for unit_classes_item_data in _unit_classes:
            unit_classes_item = ResourceUnitClass.from_dict(unit_classes_item_data)

            unit_classes.append(unit_classes_item)

        services = []
        _services = d.pop("services")
        for services_item_data in _services:
            services_item = ResourceServiceLink.from_dict(services_item_data)

            services.append(services_item)

        def _parse_owner_service_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        owner_service_id = _parse_owner_service_id(d.pop("owner_service_id"))

        is_default = d.pop("is_default")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        resource = cls(
            id=id,
            location_id=location_id,
            name=name,
            mode=mode,
            capacity=capacity,
            max_party_size=max_party_size,
            combine_across_classes=combine_across_classes,
            unit_classes=unit_classes,
            services=services,
            owner_service_id=owner_service_id,
            is_default=is_default,
            created_at=created_at,
            updated_at=updated_at,
        )

        resource.additional_properties = d
        return resource

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
