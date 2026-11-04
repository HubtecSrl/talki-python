from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypedDict, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.caller_rule_kind import CallerRuleKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="CallerRuleUpdate")


@_attrs_define
class CallerRuleUpdate:
    """A partial edit of a caller rule.

    Attributes:
        kind (CallerRuleKind | Unset): `vip` or `blocked`. A number is on one list at most at a location.
        label (None | str | Unset): Replaces the label. `null` or empty removes it.
    """

    kind: CallerRuleKind | Unset = UNSET
    label: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        label: None | str | Unset
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _kind = d.pop("kind", UNSET)
        kind: CallerRuleKind | Unset
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = CallerRuleKind(_kind)

        def _parse_label(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        label = _parse_label(d.pop("label", UNSET))

        caller_rule_update = cls(
            kind=kind,
            label=label,
        )

        caller_rule_update.additional_properties = d
        return caller_rule_update

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


# `CallerRuleUpdate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class CallerRuleUpdateDict(TypedDict, total=False):
    kind: CallerRuleKind | Literal["vip", "blocked"]
    label: str | None
