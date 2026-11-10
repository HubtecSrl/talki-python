from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentTestReply")


@_attrs_define
class AgentTestReply:
    """The assistant's answer to one test message, and where the session stands. Send `session_id` with the next message
    before `expires_at`, at most `max_turns` turns in all.

        Attributes:
            session_id (str): The session this turn belongs to; send it with the next message.
            reply (str): What the assistant answered.
            turn (int): This turn's number in the session, from 1.
            max_turns (int): The most turns a session holds; start a new one after the last.
            expires_at (datetime.datetime): When the session is dropped if no message continues it, 30 minutes after this
                turn.
            daily_remaining (int | None): Test messages the account may still send today, shared with the test in the Talki
                apps. Resets at midnight in the account's `timezone`. `null` when it could not be read.
            tools_called (list[str]): The tools the assistant used to answer, in order, by the names it sees: Talki's own
                (such as `check_availability`) and your app's, as `<prefix>__<name>`.
    """

    session_id: str
    reply: str
    turn: int
    max_turns: int
    expires_at: datetime.datetime
    daily_remaining: int | None
    tools_called: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        reply = self.reply

        turn = self.turn

        max_turns = self.max_turns

        expires_at = self.expires_at.isoformat()

        daily_remaining: int | None
        daily_remaining = self.daily_remaining

        tools_called = self.tools_called

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "session_id": session_id,
                "reply": reply,
                "turn": turn,
                "max_turns": max_turns,
                "expires_at": expires_at,
                "daily_remaining": daily_remaining,
                "tools_called": tools_called,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        session_id = d.pop("session_id")

        reply = d.pop("reply")

        turn = d.pop("turn")

        max_turns = d.pop("max_turns")

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        def _parse_daily_remaining(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        daily_remaining = _parse_daily_remaining(d.pop("daily_remaining"))

        tools_called = cast(list[str], d.pop("tools_called"))

        agent_test_reply = cls(
            session_id=session_id,
            reply=reply,
            turn=turn,
            max_turns=max_turns,
            expires_at=expires_at,
            daily_remaining=daily_remaining,
            tools_called=tools_called,
        )

        agent_test_reply.additional_properties = d
        return agent_test_reply

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
