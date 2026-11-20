from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, Required, TypedDict, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whats_app_rule import WhatsAppRule

T = TypeVar("T", bound="WhatsAppContactRuleUpdate")


@_attrs_define
class WhatsAppContactRuleUpdate:
    """A rule's new value.

    Attributes:
        rule (WhatsAppRule): `ignore`: Talki never answers the contact. `customer`: answered without judging first.
    """

    rule: WhatsAppRule
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rule = self.rule.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rule": rule,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rule = WhatsAppRule(d.pop("rule"))

        whats_app_contact_rule_update = cls(
            rule=rule,
        )

        whats_app_contact_rule_update.additional_properties = d
        return whats_app_contact_rule_update

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


# `WhatsAppContactRuleUpdate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class WhatsAppContactRuleUpdateDict(TypedDict, total=False):
    rule: Required[WhatsAppRule | Literal["ignore", "customer"]]
