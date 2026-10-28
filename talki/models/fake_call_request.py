from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Required, TypedDict, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FakeCallRequest")


@_attrs_define
class FakeCallRequest:
    """The call a sandbox should pretend it had.

    Attributes:
        scenario (str): One of the keys from `GET /v1/sandbox/scenarios`.
        caller_phone (str | Unset): The number the fake call came from. Reuse one across calls to build a caller with
            history; vary it to exercise the first-time path. At most 20 characters. Default: '+393480000001'.
    """

    scenario: str
    caller_phone: str | Unset = "+393480000001"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scenario = self.scenario

        caller_phone = self.caller_phone

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scenario": scenario,
            }
        )
        if caller_phone is not UNSET:
            field_dict["caller_phone"] = caller_phone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scenario = d.pop("scenario")

        caller_phone = d.pop("caller_phone", UNSET)

        fake_call_request = cls(
            scenario=scenario,
            caller_phone=caller_phone,
        )

        fake_call_request.additional_properties = d
        return fake_call_request

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


# `FakeCallRequest` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class FakeCallRequestDict(TypedDict, total=False):
    scenario: Required[str]
    caller_phone: str
