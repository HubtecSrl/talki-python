from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, Required, TypedDict, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whats_app_conversation_answer_answer import WhatsAppConversationAnswerAnswer

T = TypeVar("T", bound="WhatsAppConversationAnswer")


@_attrs_define
class WhatsAppConversationAnswer:
    """The owner's answer to «è un cliente?».

    Attributes:
        answer (WhatsAppConversationAnswerAnswer): `customer`: Talki answers the contact, now if WhatsApp's 24-hour
            window is still open (a `customer` rule). `ignore`: never again (an `ignore` rule). `owner`: the owner replies;
            Talki leaves the chat until the next day, no rule.
    """

    answer: WhatsAppConversationAnswerAnswer
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        answer = self.answer.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "answer": answer,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        answer = WhatsAppConversationAnswerAnswer(d.pop("answer"))

        whats_app_conversation_answer = cls(
            answer=answer,
        )

        whats_app_conversation_answer.additional_properties = d
        return whats_app_conversation_answer

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


# `WhatsAppConversationAnswer` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class WhatsAppConversationAnswerDict(TypedDict, total=False):
    answer: Required[WhatsAppConversationAnswerAnswer | Literal["customer", "ignore", "owner"]]
