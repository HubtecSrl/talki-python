from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Required, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentTestMessage")


@_attrs_define
class AgentTestMessage:
    """One message to the assistant, as a caller would say it. Omit `session_id` to start a session, and send the one from
    the reply to continue it: Talki keeps the history, and there is no way to send one. A session stays at the location
    it started at.

        Attributes:
            message (str): What the caller says, at most 1,000 characters.
            session_id (None | str | Unset): The session to continue, from an earlier reply. Omit it to start a new one.
            location_id (None | str | Unset): The location whose assistant answers, an id from `GET /v1/locations`. Omit it
                for the main location. A session stays at the location it started at: with `session_id`, send the same one or
                none.
    """

    message: str
    session_id: None | str | Unset = UNSET
    location_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        session_id: None | str | Unset
        if isinstance(self.session_id, Unset):
            session_id = UNSET
        else:
            session_id = self.session_id

        location_id: None | str | Unset
        if isinstance(self.location_id, Unset):
            location_id = UNSET
        else:
            location_id = self.location_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
            }
        )
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if location_id is not UNSET:
            field_dict["location_id"] = location_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        def _parse_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_location_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        location_id = _parse_location_id(d.pop("location_id", UNSET))

        agent_test_message = cls(
            message=message,
            session_id=session_id,
            location_id=location_id,
        )

        agent_test_message.additional_properties = d
        return agent_test_message

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


# `AgentTestMessage` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class AgentTestMessageDict(TypedDict, total=False):
    message: Required[str]
    session_id: str | None
    location_id: str | None
