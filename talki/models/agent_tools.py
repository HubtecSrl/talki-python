from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_tool import AgentTool


T = TypeVar("T", bound="AgentTools")


@_attrs_define
class AgentTools:
    """Your app's tools with an approved revision on one account, and which of them the assistant may call: the account's
    list, used at every location without its own, or one location's (`location_id`). A tool reaches a call only while it
    is in `enabled` and `owner_off` is false.

        Attributes:
            object_ (str): Always `agent_tools`.
            location_id (None | str): The location this list is for, or null for the account's list.
            inherited (bool): True when the location has no list of its own and follows the account's. Always false for the
                account's list.
            enabled (list[str]): The names of the live tools on at this level, sorted.
            owner_off (bool): Whether the account owner has switched your app's tools off on their calls. While true, no
                tool reaches a call, whatever the lists say; the lists are kept for when the owner switches them back on.
            limit_per_call (int): The most agent tools one call can have, every app of the account together.
            tools (list[AgentTool]): Every tool of your app with an approved revision, by name.
    """

    object_: str
    location_id: None | str
    inherited: bool
    enabled: list[str]
    owner_off: bool
    limit_per_call: int
    tools: list[AgentTool]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_

        location_id: None | str
        location_id = self.location_id

        inherited = self.inherited

        enabled = self.enabled

        owner_off = self.owner_off

        limit_per_call = self.limit_per_call

        tools = []
        for tools_item_data in self.tools:
            tools_item = tools_item_data.to_dict()
            tools.append(tools_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "location_id": location_id,
                "inherited": inherited,
                "enabled": enabled,
                "owner_off": owner_off,
                "limit_per_call": limit_per_call,
                "tools": tools,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_tool import AgentTool  # noqa: PLC0415

        d = dict(src_dict)
        object_ = d.pop("object")

        def _parse_location_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        location_id = _parse_location_id(d.pop("location_id"))

        inherited = d.pop("inherited")

        enabled = cast(list[str], d.pop("enabled"))

        owner_off = d.pop("owner_off")

        limit_per_call = d.pop("limit_per_call")

        tools = []
        _tools = d.pop("tools")
        for tools_item_data in _tools:
            tools_item = AgentTool.from_dict(tools_item_data)

            tools.append(tools_item)

        agent_tools = cls(
            object_=object_,
            location_id=location_id,
            inherited=inherited,
            enabled=enabled,
            owner_off=owner_off,
            limit_per_call=limit_per_call,
            tools=tools,
        )

        agent_tools.additional_properties = d
        return agent_tools

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
