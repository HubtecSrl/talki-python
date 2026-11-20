from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WhatsAppQuestion")


@_attrs_define
class WhatsAppQuestion:
    """«È un cliente?»: Talki kept silent with an unknown contact and asks the owner. Asked once per contact: while
    unanswered it moves to the contact's newest conversation (same `chat_id`), and the older one's `question` becomes
    null.

        Attributes:
            state (str): `pending` until the owner answers, then the answer: `customer`, `ignore` or `owner`.
            asked_at (datetime.datetime | None): RFC 3339 UTC.
            answered_at (datetime.datetime | None): RFC 3339 UTC, or null while pending.
    """

    state: str
    asked_at: datetime.datetime | None
    answered_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state

        asked_at: None | str
        if isinstance(self.asked_at, datetime.datetime):
            asked_at = self.asked_at.isoformat()
        else:
            asked_at = self.asked_at

        answered_at: None | str
        if isinstance(self.answered_at, datetime.datetime):
            answered_at = self.answered_at.isoformat()
        else:
            answered_at = self.answered_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "asked_at": asked_at,
                "answered_at": answered_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = d.pop("state")

        def _parse_asked_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                asked_at_type_0 = datetime.datetime.fromisoformat(data)

                return asked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        asked_at = _parse_asked_at(d.pop("asked_at"))

        def _parse_answered_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                answered_at_type_0 = datetime.datetime.fromisoformat(data)

                return answered_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        answered_at = _parse_answered_at(d.pop("answered_at"))

        whats_app_question = cls(
            state=state,
            asked_at=asked_at,
            answered_at=answered_at,
        )

        whats_app_question.additional_properties = d
        return whats_app_question

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
