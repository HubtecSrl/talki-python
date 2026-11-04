from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.unresolved_request_status import UnresolvedRequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="UnresolvedRequestUpdate")


@_attrs_define
class UnresolvedRequestUpdate:
    """A new status for an unresolved request, the answer given to the caller, or both. Send at least one.

    Attributes:
        status (UnresolvedRequestStatus | Unset): `open` — waiting on the business. `resolved` — dealt with. `dismissed`
            — closed without action.
        answer (None | str | Unset): What the business told the caller, up to 2000 characters, trimmed. Only a request
            that is `resolved`, or that this same request resolves, takes one. `null` or a blank text clears it.
    """

    status: UnresolvedRequestStatus | Unset = UNSET
    answer: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        answer: None | str | Unset
        if isinstance(self.answer, Unset):
            answer = UNSET
        else:
            answer = self.answer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if answer is not UNSET:
            field_dict["answer"] = answer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _status = d.pop("status", UNSET)
        status: UnresolvedRequestStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = UnresolvedRequestStatus(_status)

        def _parse_answer(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        answer = _parse_answer(d.pop("answer", UNSET))

        unresolved_request_update = cls(
            status=status,
            answer=answer,
        )

        unresolved_request_update.additional_properties = d
        return unresolved_request_update

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


# `UnresolvedRequestUpdate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class UnresolvedRequestUpdateDict(TypedDict, total=False):
    status: UnresolvedRequestStatus | Literal["open", "resolved", "dismissed"]
    answer: str | None
