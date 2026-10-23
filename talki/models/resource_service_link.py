from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourceServiceLink")


@_attrs_define
class ResourceServiceLink:
    """A service that draws on this resource, and how much of it one booking takes.

    Attributes:
        service_id (str): Opaque identifier of a service in `GET /v1/services`.
        rate (int): Units of this resource consumed per booked unit of the service. A booking of quantity q consumes `q
            * rate`. Usually 1; a service that occupies two stations at once has 2.
    """

    service_id: str
    rate: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_id = self.service_id

        rate = self.rate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_id": service_id,
                "rate": rate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        service_id = d.pop("service_id")

        rate = d.pop("rate")

        resource_service_link = cls(
            service_id=service_id,
            rate=rate,
        )

        resource_service_link.additional_properties = d
        return resource_service_link

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
