from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FakeCallResponse")


@_attrs_define
class FakeCallResponse:
    """The call that was recorded, and the webhook events it sent.

    Attributes:
        call_id (str): The Call this fake call produced — fetchable at `GET /v1/calls/{id}`, and the same id the
            `call.ended` delivery carries in `data.object.id`.
        scenario (str):
        caller_phone (str):
        started_at (datetime.datetime):
        ended_at (datetime.datetime):
        duration_seconds (int):
        appointment_id (None | str): The appointment this call created, moved or cancelled, if any.
        events (list[str]): The event types this call emitted. Every delivery carries `livemode: false`.
    """

    call_id: str
    scenario: str
    caller_phone: str
    started_at: datetime.datetime
    ended_at: datetime.datetime
    duration_seconds: int
    appointment_id: None | str
    events: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call_id = self.call_id

        scenario = self.scenario

        caller_phone = self.caller_phone

        started_at = self.started_at.isoformat()

        ended_at = self.ended_at.isoformat()

        duration_seconds = self.duration_seconds

        appointment_id: None | str
        appointment_id = self.appointment_id

        events = self.events

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call_id": call_id,
                "scenario": scenario,
                "caller_phone": caller_phone,
                "started_at": started_at,
                "ended_at": ended_at,
                "duration_seconds": duration_seconds,
                "appointment_id": appointment_id,
                "events": events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        call_id = d.pop("call_id")

        scenario = d.pop("scenario")

        caller_phone = d.pop("caller_phone")

        started_at = datetime.datetime.fromisoformat(d.pop("started_at"))

        ended_at = datetime.datetime.fromisoformat(d.pop("ended_at"))

        duration_seconds = d.pop("duration_seconds")

        def _parse_appointment_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        appointment_id = _parse_appointment_id(d.pop("appointment_id"))

        events = cast(list[str], d.pop("events"))

        fake_call_response = cls(
            call_id=call_id,
            scenario=scenario,
            caller_phone=caller_phone,
            started_at=started_at,
            ended_at=ended_at,
            duration_seconds=duration_seconds,
            appointment_id=appointment_id,
            events=events,
        )

        fake_call_response.additional_properties = d
        return fake_call_response

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
