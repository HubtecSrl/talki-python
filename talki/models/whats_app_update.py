from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whats_app_mode import WhatsAppMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.whats_app_schedule_range import WhatsAppScheduleRange

from collections.abc import Sequence
from typing import Literal, TypedDict

if TYPE_CHECKING:
    from ..models.whats_app_schedule_range import WhatsAppScheduleRangeDict


T = TypeVar("T", bound="WhatsAppUpdate")


@_attrs_define
class WhatsAppUpdate:
    """A change of the mode, the schedule, or both. Omitted fields stay unchanged.

    Attributes:
        mode (None | Unset | WhatsAppMode): `off`, `always` or `scheduled`. Turning the answers on from `off` needs a
            plan with WhatsApp chats and a connected number. `scheduled` needs at least one range, sent now or already
            stored.
        schedule (list[WhatsAppScheduleRange] | None | Unset): The whole schedule, replacing the stored one.
    """

    mode: None | Unset | WhatsAppMode = UNSET
    schedule: list[WhatsAppScheduleRange] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode: None | str | Unset
        if isinstance(self.mode, Unset):
            mode = UNSET
        elif isinstance(self.mode, WhatsAppMode):
            mode = self.mode.value
        else:
            mode = self.mode

        schedule: list[dict[str, Any]] | None | Unset
        if isinstance(self.schedule, Unset):
            schedule = UNSET
        elif isinstance(self.schedule, list):
            schedule = []
            for schedule_type_0_item_data in self.schedule:
                schedule_type_0_item = schedule_type_0_item_data.to_dict()
                schedule.append(schedule_type_0_item)

        else:
            schedule = self.schedule

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mode is not UNSET:
            field_dict["mode"] = mode
        if schedule is not UNSET:
            field_dict["schedule"] = schedule

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.whats_app_schedule_range import WhatsAppScheduleRange  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_mode(data: object) -> None | Unset | WhatsAppMode:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mode_type_0 = WhatsAppMode(data)

                return mode_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | WhatsAppMode, data)

        mode = _parse_mode(d.pop("mode", UNSET))

        def _parse_schedule(data: object) -> list[WhatsAppScheduleRange] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                schedule_type_0 = []
                _schedule_type_0 = data
                for schedule_type_0_item_data in _schedule_type_0:
                    schedule_type_0_item = WhatsAppScheduleRange.from_dict(schedule_type_0_item_data)

                    schedule_type_0.append(schedule_type_0_item)

                return schedule_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WhatsAppScheduleRange] | None | Unset, data)

        schedule = _parse_schedule(d.pop("schedule", UNSET))

        whats_app_update = cls(
            mode=mode,
            schedule=schedule,
        )

        whats_app_update.additional_properties = d
        return whats_app_update

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


# `WhatsAppUpdate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class WhatsAppUpdateDict(TypedDict, total=False):
    mode: WhatsAppMode | Literal["off", "always", "scheduled"] | None
    schedule: Sequence[WhatsAppScheduleRangeDict | WhatsAppScheduleRange] | None
