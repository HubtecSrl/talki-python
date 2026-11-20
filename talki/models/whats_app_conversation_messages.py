from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.whats_app_chat_message import WhatsAppChatMessage


T = TypeVar("T", bound="WhatsAppConversationMessages")


@_attrs_define
class WhatsAppConversationMessages:
    """The messages of one conversation, oldest first: the customer's, the owner's and Talki's.

    Attributes:
        conversation_id (str): The conversation.
        messages (list[WhatsAppChatMessage]): Oldest first.
        messages_expired (bool): True once the conversation is older than 30 days: the messages are deleted, the
            conversation's record stays.
    """

    conversation_id: str
    messages: list[WhatsAppChatMessage]
    messages_expired: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        conversation_id = self.conversation_id

        messages = []
        for messages_item_data in self.messages:
            messages_item = messages_item_data.to_dict()
            messages.append(messages_item)

        messages_expired = self.messages_expired

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conversation_id": conversation_id,
                "messages": messages,
                "messages_expired": messages_expired,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.whats_app_chat_message import WhatsAppChatMessage  # noqa: PLC0415

        d = dict(src_dict)
        conversation_id = d.pop("conversation_id")

        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = WhatsAppChatMessage.from_dict(messages_item_data)

            messages.append(messages_item)

        messages_expired = d.pop("messages_expired")

        whats_app_conversation_messages = cls(
            conversation_id=conversation_id,
            messages=messages,
            messages_expired=messages_expired,
        )

        whats_app_conversation_messages.additional_properties = d
        return whats_app_conversation_messages

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
