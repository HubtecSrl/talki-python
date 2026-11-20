from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whats_app_rule import WhatsAppRule

T = TypeVar("T", bound="WhatsAppContact")


@_attrs_define
class WhatsAppContact:
    """Who wrote.

    Attributes:
        name (None | str): The name the contact gave their WhatsApp profile, or null.
        phone_number (None | str): The contact's number, E.164, or null when WhatsApp did not share it (the contact uses
            a username).
        rule (None | WhatsAppRule): The account's contact rule for them, `ignore` or `customer`, or null.
    """

    name: None | str
    phone_number: None | str
    rule: None | WhatsAppRule
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: None | str
        name = self.name

        phone_number: None | str
        phone_number = self.phone_number

        rule: None | str
        if isinstance(self.rule, WhatsAppRule):
            rule = self.rule.value
        else:
            rule = self.rule

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "phone_number": phone_number,
                "rule": rule,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))

        def _parse_phone_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_number = _parse_phone_number(d.pop("phone_number"))

        def _parse_rule(data: object) -> None | WhatsAppRule:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                rule_type_0 = WhatsAppRule(data)

                return rule_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | WhatsAppRule, data)

        rule = _parse_rule(d.pop("rule"))

        whats_app_contact = cls(
            name=name,
            phone_number=phone_number,
            rule=rule,
        )

        whats_app_contact.additional_properties = d
        return whats_app_contact

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
