from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceCreate")


@_attrs_define
class ResourceCreate:
    """A new `shared` resource at one location: a count of interchangeable units, optionally drawn on by existing services
    of that location. With no `service_ids` it limits nothing until a service is linked to it, for example by `POST
    /v1/services` with `resource_ids`. Resources made of sized units are set up in Talki.

        Attributes:
            name (str): What the business calls this resource.
            capacity (int): Total units available at one time.
            service_ids (list[str] | None | Unset): Existing services that draw on this resource, one unit per booking. A
                linked service keeps any other resource it already draws on: a booking must fit all of them.
    """

    name: str
    capacity: int
    service_ids: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        capacity = self.capacity

        service_ids: list[str] | None | Unset
        if isinstance(self.service_ids, Unset):
            service_ids = UNSET
        elif isinstance(self.service_ids, list):
            service_ids = self.service_ids

        else:
            service_ids = self.service_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "capacity": capacity,
            }
        )
        if service_ids is not UNSET:
            field_dict["service_ids"] = service_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        capacity = d.pop("capacity")

        def _parse_service_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                service_ids_type_0 = cast(list[str], data)

                return service_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        service_ids = _parse_service_ids(d.pop("service_ids", UNSET))

        resource_create = cls(
            name=name,
            capacity=capacity,
            service_ids=service_ids,
        )

        resource_create.additional_properties = d
        return resource_create

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
