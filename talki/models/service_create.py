from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServiceCreate")


@_attrs_define
class ServiceCreate:
    """A new service with a fixed duration at one location, bookable at once. Send at most one of `initial_capacity`, which
    gives the service a resource of its own, or `resource_ids`, which makes it draw on resources of the same location.
    With neither, it draws on the location's default resource (`is_default`); a location with no default resource yet is
    refused with `400 invalid_parameter`. Services booked by the day or night, party sizes, buffers and exclusions are
    set up in Talki.

        Attributes:
            name (str): What the business calls this service.
            duration_minutes (int): Length of one booking, in minutes.
            description (None | str | Unset): Longer customer-facing description.
            price (None | str | Unset): Price as free text, the way the owner writes it, such as "25€" or "from 25€". Stored
                as sent.
            initial_capacity (int | None | Unset): How many bookings of this service can overlap, counting only its own.
                Talki creates a resource of that capacity for this service alone. Omit it to share the location's default
                resource, or when sending `resource_ids`.
            resource_ids (list[str] | None | Unset): Existing resources this service draws on, one unit of each per booking.
                A booking must fit every one of them. A resource that until now belonged to one other service alone becomes a
                shared resource. Omit it when sending `initial_capacity`, or to share the location's default resource.
    """

    name: str
    duration_minutes: int
    description: None | str | Unset = UNSET
    price: None | str | Unset = UNSET
    initial_capacity: int | None | Unset = UNSET
    resource_ids: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        duration_minutes = self.duration_minutes

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        price: None | str | Unset
        if isinstance(self.price, Unset):
            price = UNSET
        else:
            price = self.price

        initial_capacity: int | None | Unset
        if isinstance(self.initial_capacity, Unset):
            initial_capacity = UNSET
        else:
            initial_capacity = self.initial_capacity

        resource_ids: list[str] | None | Unset
        if isinstance(self.resource_ids, Unset):
            resource_ids = UNSET
        elif isinstance(self.resource_ids, list):
            resource_ids = self.resource_ids

        else:
            resource_ids = self.resource_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "duration_minutes": duration_minutes,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if price is not UNSET:
            field_dict["price"] = price
        if initial_capacity is not UNSET:
            field_dict["initial_capacity"] = initial_capacity
        if resource_ids is not UNSET:
            field_dict["resource_ids"] = resource_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        duration_minutes = d.pop("duration_minutes")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_price(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        price = _parse_price(d.pop("price", UNSET))

        def _parse_initial_capacity(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        initial_capacity = _parse_initial_capacity(d.pop("initial_capacity", UNSET))

        def _parse_resource_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                resource_ids_type_0 = cast(list[str], data)

                return resource_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        resource_ids = _parse_resource_ids(d.pop("resource_ids", UNSET))

        service_create = cls(
            name=name,
            duration_minutes=duration_minutes,
            description=description,
            price=price,
            initial_capacity=initial_capacity,
            resource_ids=resource_ids,
        )

        service_create.additional_properties = d
        return service_create

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
