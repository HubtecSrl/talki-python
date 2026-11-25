from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Required, TypedDict, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="AgentToolsUpdate")


@_attrs_define
class AgentToolsUpdate:
    """The list of tools to switch on, replacing the one stored at this level.

    Attributes:
        enabled (list[str] | None): The names of the live tools to switch on; every other tool is off. `[]` switches
            them all off. `null` only with `location_id`: the location drops its own list and follows the account's again.
    """

    enabled: list[str] | None

    def to_dict(self) -> dict[str, Any]:
        enabled: list[str] | None
        if isinstance(self.enabled, list):
            enabled = self.enabled

        else:
            enabled = self.enabled

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "enabled": enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_enabled(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                enabled_type_0 = cast(list[str], data)

                return enabled_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        enabled = _parse_enabled(d.pop("enabled"))

        agent_tools_update = cls(
            enabled=enabled,
        )

        return agent_tools_update


# `AgentToolsUpdate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class AgentToolsUpdateDict(TypedDict, total=False):
    enabled: Required[Sequence[str] | None]
