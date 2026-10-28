from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Required, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UnresolvedRequestTeach")


@_attrs_define
class UnresolvedRequestTeach:
    """The general answer to a resolved request's question, written as the business would say it to any caller. It is added
    to a FAQ note the business sees and edits in Talki. It is not the request's `answer`, which records what one caller
    was told, and does not change it.

        Attributes:
            question (str): The question, up to 200 characters, as callers ask it; usually the request's `question`,
                reworded for everyone. Kept on one line: line breaks and repeated spaces become one space before the length is
                counted.
            answer (str): The answer, up to 500 characters, kept on one line like the question.
            location_id (None | str | Unset): Where the assistant uses it: a location id from `GET /v1/locations`, or `all`
                for every location, which adds the entry to the FAQ of each one. Omit it for the request's own location. An
                account whose `multi_sede` is false has one FAQ, for every location: its main location's id and `all` both go
                there. An id that is not one of the account's locations is a 404.
    """

    question: str
    answer: str
    location_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question = self.question

        answer = self.answer

        location_id: None | str | Unset
        if isinstance(self.location_id, Unset):
            location_id = UNSET
        else:
            location_id = self.location_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question": question,
                "answer": answer,
            }
        )
        if location_id is not UNSET:
            field_dict["location_id"] = location_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        question = d.pop("question")

        answer = d.pop("answer")

        def _parse_location_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        location_id = _parse_location_id(d.pop("location_id", UNSET))

        unresolved_request_teach = cls(
            question=question,
            answer=answer,
            location_id=location_id,
        )

        unresolved_request_teach.additional_properties = d
        return unresolved_request_teach

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


# `UnresolvedRequestTeach` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class UnresolvedRequestTeachDict(TypedDict, total=False):
    question: Required[str]
    answer: Required[str]
    location_id: str | None
