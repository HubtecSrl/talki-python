from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, Required, TypedDict, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whats_app_rule import WhatsAppRule

T = TypeVar("T", bound="WhatsAppContactRuleCreate")


@_attrs_define
class WhatsAppContactRuleCreate:
    """A rule for a number.

    Attributes:
        phone_number (str): The number, E.164 or Italian national format. Stored as E.164.
        rule (WhatsAppRule): `ignore`: Talki never answers the contact. `customer`: answered without judging first.
    """

    phone_number: str
    rule: WhatsAppRule
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        phone_number = self.phone_number

        rule = self.rule.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "phone_number": phone_number,
                "rule": rule,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phone_number = d.pop("phone_number")

        rule = WhatsAppRule(d.pop("rule"))

        whats_app_contact_rule_create = cls(
            phone_number=phone_number,
            rule=rule,
        )

        whats_app_contact_rule_create.additional_properties = d
        return whats_app_contact_rule_create

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


# `WhatsAppContactRuleCreate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class WhatsAppContactRuleCreateDict(TypedDict, total=False):
    phone_number: Required[str]
    rule: Required[WhatsAppRule | Literal["ignore", "customer"]]
