from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.unresolved_request_status import UnresolvedRequestStatus

T = TypeVar("T", bound="UnresolvedRequest")


@_attrs_define
class UnresolvedRequest:
    """A question the assistant could not answer on a call. It told the caller someone would get back to them; `status`
    says whether the business has. `question` is the assistant's one-line record of what was asked.

        Attributes:
            id (str): Opaque Talki identifier for this request.
            location_id (str): The location the question was about: that of the call it was raised on (`Call.location_id`).
                Never null, and it never changes.
            call_id (None | str): The call it was raised on, readable through `GET /v1/calls/{id}` with `calls:read`. Null
                once that call has aged out of retention.
            caller_phone (None | str): E.164 number to call back, as presented. Null when the caller withheld it.
            question (str): What the caller wanted to know, as the assistant recorded it. One line written by the assistant,
                not a transcript and never a quote.
            status (UnresolvedRequestStatus): `open` — waiting on the business. `resolved` — dealt with. `dismissed` —
                closed without action.
            answer (None | str): What the business told the caller, noted when the request was resolved. Null when none was
                noted, and once the request is dismissed. It belongs to this request only: it does not teach the assistant
                anything.
            created_at (datetime.datetime): RFC 3339 UTC. When the call raised it.
            resolved_at (datetime.datetime | None): RFC 3339 UTC. Set when the status leaves `open`, for `dismissed` as well
                as `resolved`, and cleared if it returns to `open`. The object has no `updated_at`: its status and its answer
                are its only changes, and each sends `unresolved_request.updated`.
    """

    id: str
    location_id: str
    call_id: None | str
    caller_phone: None | str
    question: str
    status: UnresolvedRequestStatus
    answer: None | str
    created_at: datetime.datetime
    resolved_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        call_id: None | str
        call_id = self.call_id

        caller_phone: None | str
        caller_phone = self.caller_phone

        question = self.question

        status = self.status.value

        answer: None | str
        answer = self.answer

        created_at = self.created_at.isoformat()

        resolved_at: None | str
        if isinstance(self.resolved_at, datetime.datetime):
            resolved_at = self.resolved_at.isoformat()
        else:
            resolved_at = self.resolved_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "call_id": call_id,
                "caller_phone": caller_phone,
                "question": question,
                "status": status,
                "answer": answer,
                "created_at": created_at,
                "resolved_at": resolved_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("location_id")

        def _parse_call_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        call_id = _parse_call_id(d.pop("call_id"))

        def _parse_caller_phone(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        caller_phone = _parse_caller_phone(d.pop("caller_phone"))

        question = d.pop("question")

        status = UnresolvedRequestStatus(d.pop("status"))

        def _parse_answer(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        answer = _parse_answer(d.pop("answer"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_resolved_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resolved_at_type_0 = datetime.datetime.fromisoformat(data)

                return resolved_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        resolved_at = _parse_resolved_at(d.pop("resolved_at"))

        unresolved_request = cls(
            id=id,
            location_id=location_id,
            call_id=call_id,
            caller_phone=caller_phone,
            question=question,
            status=status,
            answer=answer,
            created_at=created_at,
            resolved_at=resolved_at,
        )

        unresolved_request.additional_properties = d
        return unresolved_request

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
