from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourceUnitClass")


@_attrs_define
class ResourceUnitClass:
    """`count` identical units that each hold `size` — six four-seat tables, two rooms that sleep four. Units have no
    individual identity: you can see how many exist, not which are taken.

        Attributes:
            id (str): Opaque identifier for this class of units.
            name (str): What the business calls these units.
            size (int): How much one unit of this class holds — covers at a table, people in a room, always 1 for a single-
                occupancy station.
            count (int): How many identical units of this size exist.
            combinable (bool): True when several units of this class may be joined to hold one oversized booking (two four-
                tops pushed together for six).
            combine_max (int | None): Largest number of units of this class one booking may join. Null means as many as
                exist. Meaningless when `combinable` is false.
    """

    id: str
    name: str
    size: int
    count: int
    combinable: bool
    combine_max: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        size = self.size

        count = self.count

        combinable = self.combinable

        combine_max: int | None
        combine_max = self.combine_max

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "size": size,
                "count": count,
                "combinable": combinable,
                "combine_max": combine_max,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        size = d.pop("size")

        count = d.pop("count")

        combinable = d.pop("combinable")

        def _parse_combine_max(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        combine_max = _parse_combine_max(d.pop("combine_max"))

        resource_unit_class = cls(
            id=id,
            name=name,
            size=size,
            count=count,
            combinable=combinable,
            combine_max=combine_max,
        )

        resource_unit_class.additional_properties = d
        return resource_unit_class

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
