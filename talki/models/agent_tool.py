from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_tool_kind import AgentToolKind

T = TypeVar("T", bound="AgentTool")


@_attrs_define
class AgentTool:
    """One of your app's tools, as its approved revision declares it.

    Attributes:
        name (str): The tool's name in your app's catalogue, as registered. The assistant sees it as `<prefix>__<name>`.
        description (str): What the tool does, as the assistant reads it.
        kind (AgentToolKind): `read` looks something up; `write` changes something at your app.
        logs_requests (bool): Whether the tool records a caller's request for the business. On a call that gets such a
            tool, Talki does not record unresolved requests of its own.
        revision (int): The approved revision calls use.
        enabled (bool): Whether the tool is on at this level.
    """

    name: str
    description: str
    kind: AgentToolKind
    logs_requests: bool
    revision: int
    enabled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        kind = self.kind.value

        logs_requests = self.logs_requests

        revision = self.revision

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "kind": kind,
                "logs_requests": logs_requests,
                "revision": revision,
                "enabled": enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        kind = AgentToolKind(d.pop("kind"))

        logs_requests = d.pop("logs_requests")

        revision = d.pop("revision")

        enabled = d.pop("enabled")

        agent_tool = cls(
            name=name,
            description=description,
            kind=kind,
            logs_requests=logs_requests,
            revision=revision,
            enabled=enabled,
        )

        agent_tool.additional_properties = d
        return agent_tool

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
