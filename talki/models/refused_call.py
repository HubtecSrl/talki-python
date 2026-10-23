from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call_caller import CallCaller


T = TypeVar("T", bound="RefusedCall")


@_attrs_define
class RefusedCall:
    """A call Talki refused before answering. It has no `Call` record; `action` says what the business can do about it.

    Attributes:
        id (str): Opaque identifier of the attempt.
        location_id (str): The location the call was for: the one `dialled_number` answered for when it rang, while the
            account held it or when it released it; the main location for the account's own number, or one it has no claim
            on any more. Never null.
        caller (CallCaller): Who called, as far as the account knows. Always present; its fields may be null.
            `display_name` is set only for a name the owner entered or imported, never for one the assistant heard.
        dialled_number (None | str): The Talki number that was called, E.164. It may be a number the account no longer
            holds, while the business's line still forwards to it.
        reason (str): Why the call was refused: `user_concurrency` (the plan's simultaneous calls in use); `minutes`
            (talk time used up); `entitlement` (no active subscription); `trial_suspended` (the free trial was suspended);
            `deletion_pending` (the account is scheduled for deletion); `no_user` (the number no longer belongs to the
            account); `platform_concurrency` (Talki at capacity). New reasons may be added: show an unknown one as a generic
            refusal.
        action (None | str): What the business can do about it: `cancel_deletion` (for `deletion_pending`);
            `check_forwarding` (for `no_user`); `reactivate_subscription` (for `entitlement`, `trial_suspended`);
            `upgrade_plan` (for `user_concurrency`, `minutes`). Null when there is nothing it can do. New actions may be
            added.
        attempted_at (datetime.datetime): When the call came in, RFC 3339 UTC.
    """

    id: str
    location_id: str
    caller: CallCaller
    dialled_number: None | str
    reason: str
    action: None | str
    attempted_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        caller = self.caller.to_dict()

        dialled_number: None | str
        dialled_number = self.dialled_number

        reason = self.reason

        action: None | str
        action = self.action

        attempted_at = self.attempted_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "caller": caller,
                "dialled_number": dialled_number,
                "reason": reason,
                "action": action,
                "attempted_at": attempted_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_caller import CallCaller  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("location_id")

        caller = CallCaller.from_dict(d.pop("caller"))

        def _parse_dialled_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        dialled_number = _parse_dialled_number(d.pop("dialled_number"))

        reason = d.pop("reason")

        def _parse_action(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        action = _parse_action(d.pop("action"))

        attempted_at = datetime.datetime.fromisoformat(d.pop("attempted_at"))

        refused_call = cls(
            id=id,
            location_id=location_id,
            caller=caller,
            dialled_number=dialled_number,
            reason=reason,
            action=action,
            attempted_at=attempted_at,
        )

        refused_call.additional_properties = d
        return refused_call

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
