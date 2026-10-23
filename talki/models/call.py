from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call_appointment_change import CallAppointmentChange
    from ..models.call_caller import CallCaller
    from ..models.call_transfer import CallTransfer


T = TypeVar("T", bound="Call")


@_attrs_define
class Call:
    """One inbound call the assistant answered. Its record never changes after it is written, so it appears once in the
    change feed. Only its inbox state, `read_at` and `archived_at`, changes later, and `call.updated` reports that. A
    deleted call leaves the feed and the log; `call.deleted` is its only trace.

        Attributes:
            id (str): Opaque Talki call identifier.
            location_id (str): The location the call was for: the one whose Talki number the caller dialled (`GET
                /v1/locations`). Never null: a call to the account's own number, and every call from before locations existed,
                is the main location's. It never changes.
            caller (CallCaller): Who called, as far as the account knows. Always present; its fields may be null.
                `display_name` is set only for a name the owner entered or imported, never for one the assistant heard.
            started_at (datetime.datetime): When the call ARRIVED, before the assistant picked up. RFC 3339 UTC. This is the
                ordering key for `GET /v1/calls`.
            answered_at (datetime.datetime | None): When the assistant picked up. Null when the pickup time was not
                recorded. The gap from `started_at` is ring and connection-setup time, and is not billed.
            ended_at (datetime.datetime | None): When the call was torn down. Null when the end time was not recorded; it is
                never derived from `duration_seconds`.
            duration_seconds (int | None): The billed duration in seconds, from `answered_at` to teardown: exactly what this
                call added to `GET /v1/usage` `used_seconds`, and to a billing partner's usage report. Whole seconds, the
                fraction dropped; no minimum and no rounding up to the minute, so ten 6-second calls cost 60 seconds. A 0 bills
                nothing, and neither does any call on a developer sandbox. It excludes ring and connection-setup time, so it is
                a few seconds shorter than `ended_at - started_at`, and can differ from `ended_at - answered_at` by a second or
                so. It can also differ from a carrier's own call timing. Null when the duration was not recorded.
            summary (None | str): Short natural-language summary of what the caller wanted, written by the assistant after
                the call. Null when none was produced. Not a transcript: the conversation itself is `GET
                /v1/calls/{id}/transcript`, under the separate `transcripts:read` scope.
            appointment_ids (list[str]): Appointments booked during this call, oldest first. Empty for a call that booked
                nothing. Includes appointments since cancelled — the link records what the call did, not the appointment's
                current state.
            outcome (None | str): What the call came to, one value by priority, for a list column or a filter: `booked` (it
                booked an appointment, not cancelled again on the same call), `rescheduled` (it moved an existing appointment),
                `cancelled` (it cancelled one), `transferred` (a person took the call over), `unresolved` (it left a question
                for the owner), `info` (none of these). A call that did several things takes the first; the fields below say
                everything it did. Null on calls recorded before outcomes were tracked, where the three fields below are null
                too: unknown, not empty. New values may be added.
            transfers (list[CallTransfer] | None): Every transfer to a person, in order: a caller can be passed on more than
                once. Empty when there was none.
            appointment_changes (list[CallAppointmentChange] | None): Existing appointments this call moved or cancelled, in
                order. Appointments it booked are `appointment_ids`, and a change to one of those is listed here too.
            unresolved_request_ids (list[str] | None): The questions this call left for the owner (`GET
                /v1/unresolved_requests/{id}`). Empty when there was none.
            created_at (datetime.datetime): When this record was written, RFC 3339 UTC: after the call ended, so a long call
                can be written after a shorter call that started later. `created_after` filters on this field. **Do not use it
                as a sync watermark**: records do not become visible in `created_at` order, so a watermark on it can skip a call
                permanently. Resume a sync with `GET /v1/calls?sync=true` and its cursor.
            read_at (datetime.datetime | None): When the call was first marked read, RFC 3339 UTC. Null while unread. Inbox
                state: it changes with `PATCH /v1/calls/{id}` and in the Talki app, sends `call.updated`, and does not move the
                call in the `sync=true` feed.
            archived_at (datetime.datetime | None): When the call was archived, RFC 3339 UTC. Null while it is in the inbox.
                Archiving marks the call read; marking an archived call unread clears `read_at` and leaves it archived. Inbox
                state, like `read_at`.
    """

    id: str
    location_id: str
    caller: CallCaller
    started_at: datetime.datetime
    answered_at: datetime.datetime | None
    ended_at: datetime.datetime | None
    duration_seconds: int | None
    summary: None | str
    appointment_ids: list[str]
    outcome: None | str
    transfers: list[CallTransfer] | None
    appointment_changes: list[CallAppointmentChange] | None
    unresolved_request_ids: list[str] | None
    created_at: datetime.datetime
    read_at: datetime.datetime | None
    archived_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        caller = self.caller.to_dict()

        started_at = self.started_at.isoformat()

        answered_at: None | str
        if isinstance(self.answered_at, datetime.datetime):
            answered_at = self.answered_at.isoformat()
        else:
            answered_at = self.answered_at

        ended_at: None | str
        if isinstance(self.ended_at, datetime.datetime):
            ended_at = self.ended_at.isoformat()
        else:
            ended_at = self.ended_at

        duration_seconds: int | None
        duration_seconds = self.duration_seconds

        summary: None | str
        summary = self.summary

        appointment_ids = self.appointment_ids

        outcome: None | str
        outcome = self.outcome

        transfers: list[dict[str, Any]] | None
        if isinstance(self.transfers, list):
            transfers = []
            for transfers_type_0_item_data in self.transfers:
                transfers_type_0_item = transfers_type_0_item_data.to_dict()
                transfers.append(transfers_type_0_item)

        else:
            transfers = self.transfers

        appointment_changes: list[dict[str, Any]] | None
        if isinstance(self.appointment_changes, list):
            appointment_changes = []
            for appointment_changes_type_0_item_data in self.appointment_changes:
                appointment_changes_type_0_item = appointment_changes_type_0_item_data.to_dict()
                appointment_changes.append(appointment_changes_type_0_item)

        else:
            appointment_changes = self.appointment_changes

        unresolved_request_ids: list[str] | None
        if isinstance(self.unresolved_request_ids, list):
            unresolved_request_ids = self.unresolved_request_ids

        else:
            unresolved_request_ids = self.unresolved_request_ids

        created_at = self.created_at.isoformat()

        read_at: None | str
        if isinstance(self.read_at, datetime.datetime):
            read_at = self.read_at.isoformat()
        else:
            read_at = self.read_at

        archived_at: None | str
        if isinstance(self.archived_at, datetime.datetime):
            archived_at = self.archived_at.isoformat()
        else:
            archived_at = self.archived_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "caller": caller,
                "started_at": started_at,
                "answered_at": answered_at,
                "ended_at": ended_at,
                "duration_seconds": duration_seconds,
                "summary": summary,
                "appointment_ids": appointment_ids,
                "outcome": outcome,
                "transfers": transfers,
                "appointment_changes": appointment_changes,
                "unresolved_request_ids": unresolved_request_ids,
                "created_at": created_at,
                "read_at": read_at,
                "archived_at": archived_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_appointment_change import CallAppointmentChange  # noqa: PLC0415
        from ..models.call_caller import CallCaller  # noqa: PLC0415
        from ..models.call_transfer import CallTransfer  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("location_id")

        caller = CallCaller.from_dict(d.pop("caller"))

        started_at = datetime.datetime.fromisoformat(d.pop("started_at"))

        def _parse_answered_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                answered_at_type_0 = datetime.datetime.fromisoformat(data)

                return answered_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        answered_at = _parse_answered_at(d.pop("answered_at"))

        def _parse_ended_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ended_at_type_0 = datetime.datetime.fromisoformat(data)

                return ended_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        ended_at = _parse_ended_at(d.pop("ended_at"))

        def _parse_duration_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        duration_seconds = _parse_duration_seconds(d.pop("duration_seconds"))

        def _parse_summary(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        summary = _parse_summary(d.pop("summary"))

        appointment_ids = cast(list[str], d.pop("appointment_ids"))

        def _parse_outcome(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        outcome = _parse_outcome(d.pop("outcome"))

        def _parse_transfers(data: object) -> list[CallTransfer] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                transfers_type_0 = []
                _transfers_type_0 = data
                for transfers_type_0_item_data in _transfers_type_0:
                    transfers_type_0_item = CallTransfer.from_dict(transfers_type_0_item_data)

                    transfers_type_0.append(transfers_type_0_item)

                return transfers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CallTransfer] | None, data)

        transfers = _parse_transfers(d.pop("transfers"))

        def _parse_appointment_changes(data: object) -> list[CallAppointmentChange] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                appointment_changes_type_0 = []
                _appointment_changes_type_0 = data
                for appointment_changes_type_0_item_data in _appointment_changes_type_0:
                    appointment_changes_type_0_item = CallAppointmentChange.from_dict(
                        appointment_changes_type_0_item_data
                    )

                    appointment_changes_type_0.append(appointment_changes_type_0_item)

                return appointment_changes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CallAppointmentChange] | None, data)

        appointment_changes = _parse_appointment_changes(d.pop("appointment_changes"))

        def _parse_unresolved_request_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                unresolved_request_ids_type_0 = cast(list[str], data)

                return unresolved_request_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        unresolved_request_ids = _parse_unresolved_request_ids(d.pop("unresolved_request_ids"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_read_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                read_at_type_0 = datetime.datetime.fromisoformat(data)

                return read_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        read_at = _parse_read_at(d.pop("read_at"))

        def _parse_archived_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                archived_at_type_0 = datetime.datetime.fromisoformat(data)

                return archived_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        archived_at = _parse_archived_at(d.pop("archived_at"))

        call = cls(
            id=id,
            location_id=location_id,
            caller=caller,
            started_at=started_at,
            answered_at=answered_at,
            ended_at=ended_at,
            duration_seconds=duration_seconds,
            summary=summary,
            appointment_ids=appointment_ids,
            outcome=outcome,
            transfers=transfers,
            appointment_changes=appointment_changes,
            unresolved_request_ids=unresolved_request_ids,
            created_at=created_at,
            read_at=read_at,
            archived_at=archived_at,
        )

        call.additional_properties = d
        return call

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
