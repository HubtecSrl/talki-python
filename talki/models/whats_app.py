from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whats_app_mode import WhatsAppMode

if TYPE_CHECKING:
    from ..models.whats_app_connection import WhatsAppConnection
    from ..models.whats_app_schedule_range import WhatsAppScheduleRange
    from ..models.whats_app_usage import WhatsAppUsage


T = TypeVar("T", bound="WhatsApp")


@_attrs_define
class WhatsApp:
    """The account's WhatsApp Business number and how Talki answers chats on it. Talki answers customers like a front desk,
    with the same knowledge, services, hours and calendar as on the phone, and steps back as soon as the owner writes in
    a chat. The owner connects the number in the Talki app.

        Attributes:
            connection (WhatsAppConnection): The connected WhatsApp Business number.
            mode (WhatsAppMode): `off`: Talki reads and stores nothing. `always`: Talki answers every customer. `scheduled`:
                only inside `schedule`.
            schedule (list[WhatsAppScheduleRange]): The ranges of `scheduled`. Kept when `mode` changes, so switching back
                to `scheduled` finds them.
            after_hours_schedule (list[WhatsAppScheduleRange]): Every time of the week the main location's weekly hours
                leave closed, ready to send as `schedule` for answers outside opening hours only.
            available (bool): Whether Talki can answer chats on this account: its plan includes them, and they are
                available. `blocked_reason` says why not.
            blocked_reason (None | str): Why Talki is not answering now although `mode` is not `off`, or why turning it on
                would be refused: `disabled` (not available yet), `upgrade` (the plan has no WhatsApp chats), `not_connected`
                (no number). Null when nothing stands in the way.
            usage (None | WhatsAppUsage): This period's answered conversations, or null when the plan has no chats.
            pending_questions (int): Conversations whose «è un cliente?» the owner has not answered.
            stored_conversations (int): Conversations stored, what `DELETE /v1/whatsapp/conversations` deletes.
    """

    connection: WhatsAppConnection
    mode: WhatsAppMode
    schedule: list[WhatsAppScheduleRange]
    after_hours_schedule: list[WhatsAppScheduleRange]
    available: bool
    blocked_reason: None | str
    usage: None | WhatsAppUsage
    pending_questions: int
    stored_conversations: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.whats_app_usage import WhatsAppUsage  # noqa: PLC0415

        connection = self.connection.to_dict()

        mode = self.mode.value

        schedule = []
        for schedule_item_data in self.schedule:
            schedule_item = schedule_item_data.to_dict()
            schedule.append(schedule_item)

        after_hours_schedule = []
        for after_hours_schedule_item_data in self.after_hours_schedule:
            after_hours_schedule_item = after_hours_schedule_item_data.to_dict()
            after_hours_schedule.append(after_hours_schedule_item)

        available = self.available

        blocked_reason: None | str
        blocked_reason = self.blocked_reason

        usage: dict[str, Any] | None
        if isinstance(self.usage, WhatsAppUsage):
            usage = self.usage.to_dict()
        else:
            usage = self.usage

        pending_questions = self.pending_questions

        stored_conversations = self.stored_conversations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connection": connection,
                "mode": mode,
                "schedule": schedule,
                "after_hours_schedule": after_hours_schedule,
                "available": available,
                "blocked_reason": blocked_reason,
                "usage": usage,
                "pending_questions": pending_questions,
                "stored_conversations": stored_conversations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.whats_app_connection import WhatsAppConnection  # noqa: PLC0415
        from ..models.whats_app_schedule_range import WhatsAppScheduleRange  # noqa: PLC0415
        from ..models.whats_app_usage import WhatsAppUsage  # noqa: PLC0415

        d = dict(src_dict)
        connection = WhatsAppConnection.from_dict(d.pop("connection"))

        mode = WhatsAppMode(d.pop("mode"))

        schedule = []
        _schedule = d.pop("schedule")
        for schedule_item_data in _schedule:
            schedule_item = WhatsAppScheduleRange.from_dict(schedule_item_data)

            schedule.append(schedule_item)

        after_hours_schedule = []
        _after_hours_schedule = d.pop("after_hours_schedule")
        for after_hours_schedule_item_data in _after_hours_schedule:
            after_hours_schedule_item = WhatsAppScheduleRange.from_dict(after_hours_schedule_item_data)

            after_hours_schedule.append(after_hours_schedule_item)

        available = d.pop("available")

        def _parse_blocked_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        blocked_reason = _parse_blocked_reason(d.pop("blocked_reason"))

        def _parse_usage(data: object) -> None | WhatsAppUsage:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                usage_type_0 = WhatsAppUsage.from_dict(data)

                return usage_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | WhatsAppUsage, data)

        usage = _parse_usage(d.pop("usage"))

        pending_questions = d.pop("pending_questions")

        stored_conversations = d.pop("stored_conversations")

        whats_app = cls(
            connection=connection,
            mode=mode,
            schedule=schedule,
            after_hours_schedule=after_hours_schedule,
            available=available,
            blocked_reason=blocked_reason,
            usage=usage,
            pending_questions=pending_questions,
            stored_conversations=stored_conversations,
        )

        whats_app.additional_properties = d
        return whats_app

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
