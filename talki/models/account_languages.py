from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AccountLanguages")


@_attrs_define
class AccountLanguages:
    """The languages the assistant speaks on calls, ISO 639-1. Read only: change them through `multilingual_enabled`.

    Attributes:
        primary (str): The language every call opens in, before the caller has said anything. Always `it` today.
        supported (list[str]): Every language the assistant may speak, `primary` first: `it` alone while
            `multilingual_enabled` is false, otherwise `it`, `en`, `fr`, `de` and `es`. More may be added. Read only: change
            it through `multilingual_enabled`.
    """

    primary: str
    supported: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        primary = self.primary

        supported = self.supported

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "primary": primary,
                "supported": supported,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        primary = d.pop("primary")

        supported = cast(list[str], d.pop("supported"))

        account_languages = cls(
            primary=primary,
            supported=supported,
        )

        account_languages.additional_properties = d
        return account_languages

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
