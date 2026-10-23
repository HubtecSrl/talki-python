from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call import Call


T = TypeVar("T", bound="CallList")


@_attrs_define
class CallList:
    """A page of calls. In the default newest-first list, `next_cursor` points at the next page and is null after the last.
    With `sync=true` it is your position in the change feed, returned on the last page too: store it and resume from it.

        Attributes:
            data (list[Call]):
            next_cursor (None | str): Opaque position after this page. In the default newest-first list this is a page
                pointer and is null on the last page. With `sync=true` it is your position in the change feed and is present on
                every page that returned data, including the last one — store it and pass it back as `cursor` to receive only
                what has been recorded since. Null when the page was empty. Do not parse it, and do not use a cursor from one
                mode in the other.
            has_more (bool): True when another page is available. Default: False.
    """

    data: list[Call]
    next_cursor: None | str
    has_more: bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        next_cursor: None | str
        next_cursor = self.next_cursor

        has_more = self.has_more

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "next_cursor": next_cursor,
                "has_more": has_more,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call import Call  # noqa: PLC0415

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Call.from_dict(data_item_data)

            data.append(data_item)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        has_more = d.pop("has_more")

        call_list = cls(
            data=data,
            next_cursor=next_cursor,
            has_more=has_more,
        )

        call_list.additional_properties = d
        return call_list

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
