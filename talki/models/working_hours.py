from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.working_hours_slot import WorkingHoursSlot


T = TypeVar("T", bound="WorkingHours")


@_attrs_define
class WorkingHours:
    """One location's regular weekly opening hours, the main one unless `?location_id=` names another: what the assistant
    offers that location's callers and what `GET /v1/availability` is computed from for its services. Dated exceptions
    are `Closure` objects. The response's `ETag` goes back as `If-Match` on `PUT /v1/working_hours` with the same
    `location_id`.

        Attributes:
            location_id (str): The location these are the hours of, an id from `GET /v1/locations`: the one the request
                named with `location_id`, or the main location when it named none.
            slots (list[WorkingHoursSlot]): Every weekly opening. A day with a lunch break has two slots. An empty list
                means the business has no regular opening hours, so the assistant offers callers no regular time to book.
    """

    location_id: str
    slots: list[WorkingHoursSlot]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        location_id = self.location_id

        slots = []
        for slots_item_data in self.slots:
            slots_item = slots_item_data.to_dict()
            slots.append(slots_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "location_id": location_id,
                "slots": slots,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.working_hours_slot import WorkingHoursSlot  # noqa: PLC0415

        d = dict(src_dict)
        location_id = d.pop("location_id")

        slots = []
        _slots = d.pop("slots")
        for slots_item_data in _slots:
            slots_item = WorkingHoursSlot.from_dict(slots_item_data)

            slots.append(slots_item)

        working_hours = cls(
            location_id=location_id,
            slots=slots,
        )

        working_hours.additional_properties = d
        return working_hours

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
