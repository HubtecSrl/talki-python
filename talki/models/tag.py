from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Tag")


@_attrs_define
class Tag:
    """A label on contacts. `contact_ids` are ids from `GET /v1/contacts`; `tag.updated` reports a change to the label or
    to who carries it, including a contact deleted or tagged in the Talki app.

        Attributes:
            id (str): Tag identifier.
            name (str): The label, as shown to the owner.
            color (str): The display colour, as the Talki app stores it.
            contact_ids (list[str]): The contacts that carry this tag, as `GET /v1/contacts` ids, sorted.
            created_at (datetime.datetime): When the tag was made, RFC 3339 UTC.
    """

    id: str
    name: str
    color: str
    contact_ids: list[str]
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        color = self.color

        contact_ids = self.contact_ids

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "color": color,
                "contact_ids": contact_ids,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        color = d.pop("color")

        contact_ids = cast(list[str], d.pop("contact_ids"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        tag = cls(
            id=id,
            name=name,
            color=color,
            contact_ids=contact_ids,
            created_at=created_at,
        )

        tag.additional_properties = d
        return tag

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
