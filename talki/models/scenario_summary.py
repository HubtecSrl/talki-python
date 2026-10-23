from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ScenarioSummary")


@_attrs_define
class ScenarioSummary:
    """One sandbox call scenario, and the events it emits.

    Attributes:
        key (str): The value to pass as `scenario`.
        description (str): What the caller did on this call.
        events (list[str]): The webhook event types this scenario emits, exactly. An integration test can assert on
            them.
        duration_seconds (int):
    """

    key: str
    description: str
    events: list[str]
    duration_seconds: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        description = self.description

        events = self.events

        duration_seconds = self.duration_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "description": description,
                "events": events,
                "duration_seconds": duration_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        description = d.pop("description")

        events = cast(list[str], d.pop("events"))

        duration_seconds = d.pop("duration_seconds")

        scenario_summary = cls(
            key=key,
            description=description,
            events=events,
            duration_seconds=duration_seconds,
        )

        scenario_summary.additional_properties = d
        return scenario_summary

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
