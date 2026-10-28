"""The `appointments` operations, one module each, and `AppointmentsResource` / `AsyncAppointmentsResource`,
which `Talki` and `AsyncTalki` expose as `appointments`."""

import datetime
from functools import cached_property

from ... import _resource
from ... import pagination as _pagination
from ...models.appointment import Appointment
from ...models.appointment_create import AppointmentCreate, AppointmentCreateDict
from ...models.appointment_list import AppointmentList
from ...models.appointment_reschedule import AppointmentReschedule, AppointmentRescheduleDict
from ...models.appointment_status import AppointmentStatus
from ...types import UNSET, Unset
from . import (
    cancel_appointment,
    create_appointment,
    get_appointment,
    list_appointments,
    reschedule_appointment,
    restore_appointment,
)

__all__ = [
    "AsyncAppointmentsResource",
    "AsyncAppointmentsResourceWithRawResponse",
    "AppointmentsResource",
    "AppointmentsResourceWithRawResponse",
]


class AppointmentsResourceWithRawResponse(_resource.Resource):
    """`talki.appointments.with_raw_response`: the methods of `talki.appointments`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def cancel(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.appointments.cancel`, returning the whole answer."""
        return _resource.raw(
            cancel_appointment.sync_detailed(
                client=self._client,
                appointment_id=appointment_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def create(
        self,
        *,
        body: AppointmentCreate | AppointmentCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Appointment]:
        """`talki.appointments.create`, returning the whole answer."""
        body = _resource.as_body(body, AppointmentCreate)
        return _resource.raw(
            create_appointment.sync_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def get(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Appointment]:
        """`talki.appointments.get`, returning the whole answer."""
        return _resource.raw(
            get_appointment.sync_detailed(
                client=self._client,
                appointment_id=appointment_id,
                talki_version=talki_version,
            )
        )

    def reschedule(
        self,
        appointment_id: str,
        *,
        body: AppointmentReschedule | AppointmentRescheduleDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Appointment]:
        """`talki.appointments.reschedule`, returning the whole answer."""
        body = _resource.as_body(body, AppointmentReschedule)
        return _resource.raw(
            reschedule_appointment.sync_detailed(
                client=self._client,
                appointment_id=appointment_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def restore(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Appointment]:
        """`talki.appointments.restore`, returning the whole answer."""
        return _resource.raw(
            restore_appointment.sync_detailed(
                client=self._client,
                appointment_id=appointment_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        status: AppointmentStatus | None | Unset = UNSET,
        starts_after: datetime.datetime | None | Unset = UNSET,
        starts_before: datetime.datetime | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.Page[Appointment]]:
        """`talki.appointments.list`, returning the whole answer."""

        def fetch(cursor: None | str | Unset) -> AppointmentList:
            return _resource.unwrap(
                list_appointments.sync_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    status=status,
                    starts_after=starts_after,
                    starts_before=starts_before,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            list_appointments.sync_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                status=status,
                starts_after=starts_after,
                starts_before=starts_before,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.Page(page, fetch, cursor))


class AppointmentsResource(_resource.Resource):
    """`talki.appointments`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AppointmentsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AppointmentsResourceWithRawResponse(self._client)

    def cancel(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Cancel an appointment

         Mark a booking cancelled without deleting it. Requires `Idempotency-Key`. Requires
        `appointments:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            appointment_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            self.with_raw_response.cancel(
                appointment_id=appointment_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def create(
        self,
        *,
        body: AppointmentCreate | AppointmentCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Appointment:
        """Create an appointment

         Book through the same capacity rules as the Talki assistant, at the location of the service (the
        main location without one). A service of an inactive location is refused with `location_inactive`.
        Requires `Idempotency-Key`. Requires `appointments:write`. Limited to 120 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (AppointmentCreate | AppointmentCreateDict): A booking to create: one service per appointment, booked at that
                service's location. `notes` is visible to the business and stored on the booking.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Appointment
        """
        return (
            self.with_raw_response.create(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def get(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Appointment:
        """Retrieve an appointment

         Return one active or cancelled appointment belonging to the account. Requires `appointments:read`.
        Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            appointment_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Appointment
        """
        return (
            self.with_raw_response.get(
                appointment_id=appointment_id,
                talki_version=talki_version,
            )
        ).parse()

    def reschedule(
        self,
        appointment_id: str,
        *,
        body: AppointmentReschedule | AppointmentRescheduleDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Appointment:
        """Update an appointment

         Move or rename a booking while keeping its ID. A move is refused with `service_deleted` when a
        service of the booking has been deleted and the move would make that service's part of the booking
        end in the future, and with `location_inactive` when the booking's location is switched off; such a
        booking can still be renamed. Requires `Idempotency-Key`. Requires `appointments:write`. Limited to
        120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            appointment_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (AppointmentReschedule | AppointmentRescheduleDict): A partial edit of a booking. Every field is optional, and an
                omitted field is left unchanged, not cleared. A move that does not fit is refused with a
                conflict code; nothing is booked. A booking never changes location.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Appointment
        """
        return (
            self.with_raw_response.reschedule(
                appointment_id=appointment_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def restore(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Appointment:
        """Restore an appointment

         Undo a cancellation, keeping the ID. Refused with a conflict code when the time no longer fits, and
        with `service_deleted` when a service of the booking has been deleted and that service's part of the
        booking ends in the future: book it again with a service that exists. Refused with
        `location_inactive` when the booking's location is switched off. Requires `Idempotency-Key`.
        Requires `appointments:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            appointment_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Appointment
        """
        return (
            self.with_raw_response.restore(
                appointment_id=appointment_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        status: AppointmentStatus | None | Unset = UNSET,
        starts_after: datetime.datetime | None | Unset = UNSET,
        starts_before: datetime.datetime | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[Appointment]:
        """List appointment changes

         Walk the appointment change feed in commit order. Store `next_cursor` even on the last non-empty
        page. Requires `appointments:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of appointments to return. Default: 50.
            cursor (None | str | Unset): Opaque position in the change feed, from a previous
                response's `next_cursor`. Omit to start from the beginning. Store the last one you
                received: it is how you resume a sync without re-reading everything. Not interchangeable
                with a `GET /v1/calls` cursor.
            status (AppointmentStatus | None | Unset): Restrict to `active` or `cancelled`. Omit to
                get both — which is what an incremental sync needs, since a cancellation is a change you
                must see. Use this only for a point-in-time snapshot.
            starts_after (datetime.datetime | None | Unset): Only appointments starting at or after
                this instant (RFC 3339 UTC). A filter on WHEN THE BOOKING IS, not on when it changed; it
                does not affect ordering and must not be used as a sync watermark.
            starts_before (datetime.datetime | None | Unset): Only appointments starting strictly
                before this instant (RFC 3339 UTC).
            location_id (None | str | Unset): Only the records of this location, an id from `GET
                /v1/locations` (inactive ones included). Omit for every location: each record carries its
                `location_id`. Allowed on the change feed, because a record never changes location; a
                cursor is then bound to the location it was issued for, and refused with `invalid_cursor`
                under another `location_id` or without one.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Page[Appointment]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """
        return (
            self.with_raw_response.list(
                limit=limit,
                cursor=cursor,
                status=status,
                starts_after=starts_after,
                starts_before=starts_before,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()


class AsyncAppointmentsResourceWithRawResponse(_resource.Resource):
    """`talki.appointments.with_raw_response` on `AsyncTalki`: the methods of `talki.appointments`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def cancel(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.appointments.cancel`, returning the whole answer."""
        return _resource.raw(
            await cancel_appointment.asyncio_detailed(
                client=self._client,
                appointment_id=appointment_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def create(
        self,
        *,
        body: AppointmentCreate | AppointmentCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Appointment]:
        """`talki.appointments.create`, returning the whole answer."""
        body = _resource.as_body(body, AppointmentCreate)
        return _resource.raw(
            await create_appointment.asyncio_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def get(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Appointment]:
        """`talki.appointments.get`, returning the whole answer."""
        return _resource.raw(
            await get_appointment.asyncio_detailed(
                client=self._client,
                appointment_id=appointment_id,
                talki_version=talki_version,
            )
        )

    async def reschedule(
        self,
        appointment_id: str,
        *,
        body: AppointmentReschedule | AppointmentRescheduleDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Appointment]:
        """`talki.appointments.reschedule`, returning the whole answer."""
        body = _resource.as_body(body, AppointmentReschedule)
        return _resource.raw(
            await reschedule_appointment.asyncio_detailed(
                client=self._client,
                appointment_id=appointment_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def restore(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Appointment]:
        """`talki.appointments.restore`, returning the whole answer."""
        return _resource.raw(
            await restore_appointment.asyncio_detailed(
                client=self._client,
                appointment_id=appointment_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        status: AppointmentStatus | None | Unset = UNSET,
        starts_after: datetime.datetime | None | Unset = UNSET,
        starts_before: datetime.datetime | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.AsyncPage[Appointment]]:
        """`talki.appointments.list`, returning the whole answer."""

        async def fetch(cursor: None | str | Unset) -> AppointmentList:
            return _resource.unwrap(
                await list_appointments.asyncio_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    status=status,
                    starts_after=starts_after,
                    starts_before=starts_before,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            await list_appointments.asyncio_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                status=status,
                starts_after=starts_after,
                starts_before=starts_before,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.AsyncPage(page, fetch, cursor))


class AsyncAppointmentsResource(_resource.Resource):
    """`talki.appointments` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncAppointmentsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncAppointmentsResourceWithRawResponse(self._client)

    async def cancel(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Cancel an appointment

         Mark a booking cancelled without deleting it. Requires `Idempotency-Key`. Requires
        `appointments:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            appointment_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            await self.with_raw_response.cancel(
                appointment_id=appointment_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def create(
        self,
        *,
        body: AppointmentCreate | AppointmentCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Appointment:
        """Create an appointment

         Book through the same capacity rules as the Talki assistant, at the location of the service (the
        main location without one). A service of an inactive location is refused with `location_inactive`.
        Requires `Idempotency-Key`. Requires `appointments:write`. Limited to 120 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (AppointmentCreate | AppointmentCreateDict): A booking to create: one service per appointment, booked at that
                service's location. `notes` is visible to the business and stored on the booking.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Appointment
        """
        return (
            await self.with_raw_response.create(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def get(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Appointment:
        """Retrieve an appointment

         Return one active or cancelled appointment belonging to the account. Requires `appointments:read`.
        Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            appointment_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Appointment
        """
        return (
            await self.with_raw_response.get(
                appointment_id=appointment_id,
                talki_version=talki_version,
            )
        ).parse()

    async def reschedule(
        self,
        appointment_id: str,
        *,
        body: AppointmentReschedule | AppointmentRescheduleDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Appointment:
        """Update an appointment

         Move or rename a booking while keeping its ID. A move is refused with `service_deleted` when a
        service of the booking has been deleted and the move would make that service's part of the booking
        end in the future, and with `location_inactive` when the booking's location is switched off; such a
        booking can still be renamed. Requires `Idempotency-Key`. Requires `appointments:write`. Limited to
        120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            appointment_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (AppointmentReschedule | AppointmentRescheduleDict): A partial edit of a booking. Every field is optional, and an
                omitted field is left unchanged, not cleared. A move that does not fit is refused with a
                conflict code; nothing is booked. A booking never changes location.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Appointment
        """
        return (
            await self.with_raw_response.reschedule(
                appointment_id=appointment_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def restore(
        self,
        appointment_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Appointment:
        """Restore an appointment

         Undo a cancellation, keeping the ID. Refused with a conflict code when the time no longer fits, and
        with `service_deleted` when a service of the booking has been deleted and that service's part of the
        booking ends in the future: book it again with a service that exists. Refused with
        `location_inactive` when the booking's location is switched off. Requires `Idempotency-Key`.
        Requires `appointments:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            appointment_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Appointment
        """
        return (
            await self.with_raw_response.restore(
                appointment_id=appointment_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        status: AppointmentStatus | None | Unset = UNSET,
        starts_after: datetime.datetime | None | Unset = UNSET,
        starts_before: datetime.datetime | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPager[Appointment]:
        """List appointment changes

         Walk the appointment change feed in commit order. Store `next_cursor` even on the last non-empty
        page. Requires `appointments:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of appointments to return. Default: 50.
            cursor (None | str | Unset): Opaque position in the change feed, from a previous
                response's `next_cursor`. Omit to start from the beginning. Store the last one you
                received: it is how you resume a sync without re-reading everything. Not interchangeable
                with a `GET /v1/calls` cursor.
            status (AppointmentStatus | None | Unset): Restrict to `active` or `cancelled`. Omit to
                get both — which is what an incremental sync needs, since a cancellation is a change you
                must see. Use this only for a point-in-time snapshot.
            starts_after (datetime.datetime | None | Unset): Only appointments starting at or after
                this instant (RFC 3339 UTC). A filter on WHEN THE BOOKING IS, not on when it changed; it
                does not affect ordering and must not be used as a sync watermark.
            starts_before (datetime.datetime | None | Unset): Only appointments starting strictly
                before this instant (RFC 3339 UTC).
            location_id (None | str | Unset): Only the records of this location, an id from `GET
                /v1/locations` (inactive ones included). Omit for every location: each record carries its
                `location_id`. Allowed on the change feed, because a record never changes location; a
                cursor is then bound to the location it was issued for, and refused with `invalid_cursor`
                under another `location_id` or without one.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AsyncPager[Appointment]: Awaited, this page (an `AsyncPage`). Iterated with `async for`,
            every row from here on, fetching the pages as it goes.
        """

        async def first() -> _pagination.AsyncPage[Appointment]:
            return (
                await self.with_raw_response.list(
                    limit=limit,
                    cursor=cursor,
                    status=status,
                    starts_after=starts_after,
                    starts_before=starts_before,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            ).parse()

        return _pagination.AsyncPager(first)
