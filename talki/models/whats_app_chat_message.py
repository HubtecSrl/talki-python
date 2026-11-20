from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WhatsAppChatMessage")


@_attrs_define
class WhatsAppChatMessage:
    """One message of a WhatsApp conversation.

    Attributes:
        id (str): Message identifier.
        direction (str): `customer`, `owner` (written by the owner in the WhatsApp Business app) or `talki`.
        type_ (str): WhatsApp's message type: `text`, `audio`, `image`, `document`, `reaction`, …
        text (None | str): The text. A voice note's is its automatic transcript. Null for media Talki does not read.
        created_at (datetime.datetime): RFC 3339 UTC.
        failed (bool): True for a reply of Talki's that never reached the customer.
    """

    id: str
    direction: str
    type_: str
    text: None | str
    created_at: datetime.datetime
    failed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        direction = self.direction

        type_ = self.type_

        text: None | str
        text = self.text

        created_at = self.created_at.isoformat()

        failed = self.failed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "direction": direction,
                "type": type_,
                "text": text,
                "created_at": created_at,
                "failed": failed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        direction = d.pop("direction")

        type_ = d.pop("type")

        def _parse_text(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        text = _parse_text(d.pop("text"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        failed = d.pop("failed")

        whats_app_chat_message = cls(
            id=id,
            direction=direction,
            type_=type_,
            text=text,
            created_at=created_at,
            failed=failed,
        )

        whats_app_chat_message.additional_properties = d
        return whats_app_chat_message

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
