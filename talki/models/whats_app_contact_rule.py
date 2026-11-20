from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whats_app_rule import WhatsAppRule

T = TypeVar("T", bound="WhatsAppContactRule")


@_attrs_define
class WhatsAppContactRule:
    """A contact Talki never answers (`ignore`), or answers as a customer without judging first (`customer`). One list for
    the account, at most 500 rules.

        Attributes:
            id (str): Rule identifier.
            phone_number (None | str): The number, E.164. Null for a rule set by answering «è un cliente?» about a contact
                whose number WhatsApp did not share.
            contact_name (None | str): The contact's WhatsApp profile name, when they have written.
            rule (WhatsAppRule): `ignore`: Talki never answers the contact. `customer`: answered without judging first.
            source (str): How it was set: `owner` (added by number), `activation` (when the answers were turned on),
                `question` (an answer to «è un cliente?»), `suggestion`.
            created_at (datetime.datetime): RFC 3339 UTC.
            updated_at (datetime.datetime): RFC 3339 UTC.
    """

    id: str
    phone_number: None | str
    contact_name: None | str
    rule: WhatsAppRule
    source: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        phone_number: None | str
        phone_number = self.phone_number

        contact_name: None | str
        contact_name = self.contact_name

        rule = self.rule.value

        source = self.source

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "phone_number": phone_number,
                "contact_name": contact_name,
                "rule": rule,
                "source": source,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_phone_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_number = _parse_phone_number(d.pop("phone_number"))

        def _parse_contact_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        contact_name = _parse_contact_name(d.pop("contact_name"))

        rule = WhatsAppRule(d.pop("rule"))

        source = d.pop("source")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        whats_app_contact_rule = cls(
            id=id,
            phone_number=phone_number,
            contact_name=contact_name,
            rule=rule,
            source=source,
            created_at=created_at,
            updated_at=updated_at,
        )

        whats_app_contact_rule.additional_properties = d
        return whats_app_contact_rule

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
