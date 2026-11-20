from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.whats_app_contact import WhatsAppContact
    from ..models.whats_app_question import WhatsAppQuestion


T = TypeVar("T", bound="WhatsAppConversation")


@_attrs_define
class WhatsAppConversation:
    """One conversation with one contact, from their first message until about 30 minutes after the last. Talki answers
    known customers; with an unknown contact it first judges whether they write about the business, and when they do not
    it keeps silent and asks the owner «è un cliente?» (`question`). The record stays as long as a call's; its messages
    are kept 30 days.

        Attributes:
            id (str): Conversation identifier.
            chat_id (str): The chat with this contact: the same for each of their conversations.
            contact (WhatsAppContact): Who wrote.
            started_at (datetime.datetime): The contact's first message, RFC 3339 UTC.
            ended_at (datetime.datetime | None): When the conversation closed, about 30 minutes after its last message, RFC
                3339 UTC. Null while open.
            summary (None | str): A short summary, in Italian, written when it closes and only when Talki replied or handed
                the chat to the owner. Null otherwise.
            outcome (str): What Talki did: `answered`, `handed_over` (passed to the owner), `silent_*` (not a customer:
                `silent_personal`, `silent_unsure`, `silent_spam`, `silent_supplier`), `skipped_*` (a rule kept Talki out, e.g.
                `skipped_owner_replied`, `skipped_out_of_schedule`, `skipped_cap_reached`), `dropped` (the owner wrote first),
                `failed`, `no_reply`, `merged`. Provisional while the conversation is open. Treat a value you do not know as
                Talki not having answered.
            relevance (None | str): Talki's reading of an unknown contact: `business`, `personal`, `unsure` or
                `greeting_only`. Null for a known customer, who is not checked.
            category (None | str): Who the unknown contact seemed to be, e.g. `customer`, `supplier_vendor`, or null.
            replies (int): Replies Talki sent in it.
            paused_until (None | str): Until when Talki leaves the chat to the owner, who wrote in it, RFC 3339 UTC; null
                when Talki is not paused.
            question (None | WhatsAppQuestion): The owner's «è un cliente?» about the contact, or null when not asked.
            appointment_ids (list[str]): Appointments booked in it (`GET /v1/appointments/{id}`).
    """

    id: str
    chat_id: str
    contact: WhatsAppContact
    started_at: datetime.datetime
    ended_at: datetime.datetime | None
    summary: None | str
    outcome: str
    relevance: None | str
    category: None | str
    replies: int
    paused_until: None | str
    question: None | WhatsAppQuestion
    appointment_ids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.whats_app_question import WhatsAppQuestion  # noqa: PLC0415

        id = self.id

        chat_id = self.chat_id

        contact = self.contact.to_dict()

        started_at = self.started_at.isoformat()

        ended_at: None | str
        if isinstance(self.ended_at, datetime.datetime):
            ended_at = self.ended_at.isoformat()
        else:
            ended_at = self.ended_at

        summary: None | str
        summary = self.summary

        outcome = self.outcome

        relevance: None | str
        relevance = self.relevance

        category: None | str
        category = self.category

        replies = self.replies

        paused_until: None | str
        paused_until = self.paused_until

        question: dict[str, Any] | None
        if isinstance(self.question, WhatsAppQuestion):
            question = self.question.to_dict()
        else:
            question = self.question

        appointment_ids = self.appointment_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "chat_id": chat_id,
                "contact": contact,
                "started_at": started_at,
                "ended_at": ended_at,
                "summary": summary,
                "outcome": outcome,
                "relevance": relevance,
                "category": category,
                "replies": replies,
                "paused_until": paused_until,
                "question": question,
                "appointment_ids": appointment_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.whats_app_contact import WhatsAppContact  # noqa: PLC0415
        from ..models.whats_app_question import WhatsAppQuestion  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        chat_id = d.pop("chat_id")

        contact = WhatsAppContact.from_dict(d.pop("contact"))

        started_at = datetime.datetime.fromisoformat(d.pop("started_at"))

        def _parse_ended_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ended_at_type_0 = datetime.datetime.fromisoformat(data)

                return ended_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        ended_at = _parse_ended_at(d.pop("ended_at"))

        def _parse_summary(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        summary = _parse_summary(d.pop("summary"))

        outcome = d.pop("outcome")

        def _parse_relevance(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        relevance = _parse_relevance(d.pop("relevance"))

        def _parse_category(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        category = _parse_category(d.pop("category"))

        replies = d.pop("replies")

        def _parse_paused_until(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        paused_until = _parse_paused_until(d.pop("paused_until"))

        def _parse_question(data: object) -> None | WhatsAppQuestion:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                question_type_0 = WhatsAppQuestion.from_dict(data)

                return question_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | WhatsAppQuestion, data)

        question = _parse_question(d.pop("question"))

        appointment_ids = cast(list[str], d.pop("appointment_ids"))

        whats_app_conversation = cls(
            id=id,
            chat_id=chat_id,
            contact=contact,
            started_at=started_at,
            ended_at=ended_at,
            summary=summary,
            outcome=outcome,
            relevance=relevance,
            category=category,
            replies=replies,
            paused_until=paused_until,
            question=question,
            appointment_ids=appointment_ids,
        )

        whats_app_conversation.additional_properties = d
        return whats_app_conversation

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
