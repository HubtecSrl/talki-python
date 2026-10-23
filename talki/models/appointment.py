from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.appointment_status import AppointmentStatus

if TYPE_CHECKING:
    from ..models.appointment_client import AppointmentClient
    from ..models.service_ref import ServiceRef


T = TypeVar("T", bound="Appointment")


@_attrs_define
class Appointment:
    """One booking in the account's calendar. This object is the record: a connected Google or Outlook calendar holds a
    copy, so reconcile against this object, not against the provider calendar.

        Attributes:
            id (str): Opaque Talki appointment identifier.
            location_id (str): The location the booking is at (`GET /v1/locations`), the one its service belongs to. Never
                null, and it never changes: moving a booking keeps its location.
            status (AppointmentStatus): `active` or `cancelled`. A cancelled appointment is kept, and can be restored to
                `active`.
            client (AppointmentClient): Who the booking is for. Always present; `contact_id` and `phone_number` are null for
                a booking entered by hand. The name is the one the booking was taken under, exactly as the owner sees it, and
                may come from what the assistant heard on the call.
            service (None | ServiceRef): The service booked. After the service is deleted it keeps its name with a null
                `id`. Null for an appointment taken without one (a generic slot), or whose service was deleted before Talki kept
                the name.
            start_at (datetime.datetime): Start of the booking, RFC 3339 UTC.
            end_at (datetime.datetime): End of the booking, RFC 3339 UTC. For a multi-day stay this is the check-out moment,
                so the span covers the whole booking rather than one night.
            quantity (int): Party size the booking carries — covers, people, items — for a service that asks for one
                (`asks_quantity` on `GET /v1/services`). Always 1 for a service that does not, so you can read it
                unconditionally. It is the booking's total, not a breakdown per resource or unit.
            call_id (None | str): The call this booking was taken on, or null when it was not made on a call (entered in the
                Talki app or created through this API).
            created_at (datetime.datetime): When the booking was written, RFC 3339 UTC.
            updated_at (datetime.datetime): Last change to the booking, RFC 3339 UTC. Show it to a human as "last modified";
                **do not sync on it**: changes do not become visible in `updated_at` order, so a watermark on it can skip a
                booking permanently. Use the change feed's `next_cursor` instead.
    """

    id: str
    location_id: str
    status: AppointmentStatus
    client: AppointmentClient
    service: None | ServiceRef
    start_at: datetime.datetime
    end_at: datetime.datetime
    quantity: int
    call_id: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.service_ref import ServiceRef  # noqa: PLC0415

        id = self.id

        location_id = self.location_id

        status = self.status.value

        client = self.client.to_dict()

        service: dict[str, Any] | None
        if isinstance(self.service, ServiceRef):
            service = self.service.to_dict()
        else:
            service = self.service

        start_at = self.start_at.isoformat()

        end_at = self.end_at.isoformat()

        quantity = self.quantity

        call_id: None | str
        call_id = self.call_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "status": status,
                "client": client,
                "service": service,
                "start_at": start_at,
                "end_at": end_at,
                "quantity": quantity,
                "call_id": call_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.appointment_client import AppointmentClient  # noqa: PLC0415
        from ..models.service_ref import ServiceRef  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("location_id")

        status = AppointmentStatus(d.pop("status"))

        client = AppointmentClient.from_dict(d.pop("client"))

        def _parse_service(data: object) -> None | ServiceRef:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_type_0 = ServiceRef.from_dict(data)

                return service_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ServiceRef, data)

        service = _parse_service(d.pop("service"))

        start_at = datetime.datetime.fromisoformat(d.pop("start_at"))

        end_at = datetime.datetime.fromisoformat(d.pop("end_at"))

        quantity = d.pop("quantity")

        def _parse_call_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        call_id = _parse_call_id(d.pop("call_id"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        appointment = cls(
            id=id,
            location_id=location_id,
            status=status,
            client=client,
            service=service,
            start_at=start_at,
            end_at=end_at,
            quantity=quantity,
            call_id=call_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        appointment.additional_properties = d
        return appointment

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
