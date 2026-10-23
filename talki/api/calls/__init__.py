"""The `calls` operations, one module each, and `CallsResource` / `AsyncCallsResource`,
which `Talki` and `AsyncTalki` expose as `calls`."""

import datetime

from ... import _resource
from ... import pagination as _pagination
from ...models.call import Call
from ...models.call_count import CallCount
from ...models.call_list import CallList
from ...models.call_outcome import CallOutcome
from ...models.call_stats import CallStats
from ...models.call_transcript import CallTranscript
from ...models.call_update import CallUpdate
from ...models.export_format import ExportFormat
from ...models.inbox_status import InboxStatus
from ...models.mark_all_read_result import MarkAllReadResult
from ...models.refused_call import RefusedCall
from ...models.refused_call_list import RefusedCallList
from ...models.refused_call_summary import RefusedCallSummary
from ...types import UNSET, File, Unset
from . import (
    count_calls,
    count_refused_calls,
    delete_call,
    export_call,
    export_calls,
    get_call,
    get_call_stats,
    get_call_transcript,
    get_refused_call_summary,
    list_calls,
    list_refused_calls,
    mark_all_calls_read,
    update_call,
)

__all__ = ["AsyncCallsResource", "CallsResource"]


class CallsResource(_resource.Resource):
    """`talki.calls`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    def count(
        self,
        *,
        status: InboxStatus | Unset = InboxStatus.ALL,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> CallCount:
        """Count calls

         Count the calls in one inbox view. `status=unread` is the unread badge. Requires `calls:read`.
        Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
                and not yet read. `archived` — archived calls. `all` — every call. Default:
                InboxStatus.ALL.
            location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
                id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallCount
        """
        return _resource.unwrap(
            count_calls.sync_detailed(
                client=self._client,
                status=status,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    def count_refused(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> CallCount:
        """Count refused calls

         Count every refused call the account has. Requires `calls:read`. Limited to 600 requests per minute
        per account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): Only the refused calls of this location
                (`RefusedCall.location_id`), an id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallCount
        """
        return _resource.unwrap(
            count_refused_calls.sync_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    def delete(
        self,
        call_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a call

         Delete a call for good, when the caller asks to be forgotten: the call, its transcript, the
        questions it left and the pending contacts it proposed. The appointments it booked stay, with
        `call_id` null. The talk time it used stays on the meter of `GET /v1/usage` and, for a partner-
        managed account, in the partner's usage report; `GET /v1/usage/history` and the call statistics no
        longer count the call. Sends `call.deleted`. Requires `calls:delete`. Limited to 120 requests per
        minute per account (API key) or per installation (OAuth).

        Args:
            call_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        _resource.unwrap(
            delete_call.sync_detailed(
                client=self._client,
                call_id=call_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def export_call(
        self,
        call_id: str,
        *,
        format_: ExportFormat | Unset = ExportFormat.PDF,
        talki_version: str | Unset = UNSET,
    ) -> File:
        """Export a call

         Return one call as a PDF or Excel file, on every plan. It includes the conversation only with
        `transcripts:read` and when the account keeps transcripts, and the call's appointments only with
        `appointments:read`. Requires `calls:read`. Limited to 600 requests per minute per account (API key)
        or per installation (OAuth), and to 10 file exports per minute.

        Args:
            call_id (str):
            format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
                ExportFormat.PDF.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            File
        """
        return _resource.unwrap(
            export_call.sync_detailed(
                client=self._client,
                call_id=call_id,
                format_=format_,
                talki_version=talki_version,
            )
        )

    def export_calls(
        self,
        *,
        from_: datetime.date,
        to: datetime.date,
        format_: ExportFormat | Unset = ExportFormat.PDF,
        status: InboxStatus | Unset = InboxStatus.ALL,
        q: None | str | Unset = UNSET,
        outcome: CallOutcome | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> File:
        """Export the call log

         Return the calls of a date range as a PDF or Excel file, without transcripts. `status` defaults to
        `all`; `status`, `q` and `outcome` narrow the file as they narrow `GET /v1/calls`. Each call's
        appointments are included only when the credential also holds `appointments:read`. Needs a plan that
        includes the call log export. Requires `calls:read`. Limited to 600 requests per minute per account
        (API key) or per installation (OAuth), and to 10 file exports per minute.

        Args:
            from_ (datetime.date): First day, `YYYY-MM-DD`, local to the account's `timezone`.
            to (datetime.date): Last day, included, `YYYY-MM-DD`. At most 366 days after `from`.
            format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
                ExportFormat.PDF.
            status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
                and not yet read. `archived` — archived calls. `all` — every call. Default:
                InboxStatus.ALL.
            q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
                contains it, or whose caller's `display_name` does. A name that is not published as
                `display_name` is not searched either.
            outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
                `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
                outcomes were tracked have none and match no value.
            location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
                id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            File
        """
        return _resource.unwrap(
            export_calls.sync_detailed(
                client=self._client,
                from_=from_,
                to=to,
                format_=format_,
                status=status,
                q=q,
                outcome=outcome,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    def get(
        self,
        call_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Call:
        """Retrieve a call

         Return one call belonging to the authenticated account. Requires `calls:read`. Limited to 600
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            call_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Call
        """
        return _resource.unwrap(
            get_call.sync_detailed(
                client=self._client,
                call_id=call_id,
                talki_version=talki_version,
            )
        )

    def get_stats(
        self,
        *,
        days: int | None | Unset = UNSET,
        from_: datetime.date | None | Unset = UNSET,
        to: datetime.date | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> CallStats:
        """Retrieve call statistics

         Return totals, the daily series and the top callers over the last `days`, or over the local days
        `from` to `to` (at most 366). Requires `calls:read`. Limited to 600 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            days (int | None | Unset): Length of the period, in days, ending now. Default 30. Cannot
                be combined with `from` / `to`.
            from_ (datetime.date | None | Unset): First day of the period, `YYYY-MM-DD`, local to the
                account's `timezone`. Sent with `to`, instead of `days`.
            to (datetime.date | None | Unset): Last day of the period, included, `YYYY-MM-DD`. At most
                366 days after `from`.
            location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
                id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallStats
        """
        return _resource.unwrap(
            get_call_stats.sync_detailed(
                client=self._client,
                days=days,
                from_=from_,
                to=to,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    def get_transcript(
        self,
        call_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> CallTranscript:
        """Retrieve a call transcript

         Return the automatic transcript of one call. `calls:read` does not grant it: the account owner ticks
        `transcripts:read` on its own. Requires `transcripts:read`. Limited to 600 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            call_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallTranscript
        """
        return _resource.unwrap(
            get_call_transcript.sync_detailed(
                client=self._client,
                call_id=call_id,
                talki_version=talki_version,
            )
        )

    def get_refused_summary(
        self,
        *,
        days: int | None | Unset = UNSET,
        from_: datetime.date | None | Unset = UNSET,
        to: datetime.date | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> RefusedCallSummary:
        """Summarise refused calls

         Return refused calls over the last `days`, or over the local days `from` to `to`, by reason, and the
        actions they call for. Requires `calls:read`. Limited to 600 requests per minute per account (API
        key) or per installation (OAuth).

        Args:
            days (int | None | Unset): Length of the period, in days, ending now. Default 30. Cannot
                be combined with `from` / `to`.
            from_ (datetime.date | None | Unset): First day of the period, `YYYY-MM-DD`, local to the
                account's `timezone`. Sent with `to`, instead of `days`.
            to (datetime.date | None | Unset): Last day of the period, included, `YYYY-MM-DD`. At most
                366 days after `from`.
            location_id (None | str | Unset): Only the refused calls of this location
                (`RefusedCall.location_id`), an id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            RefusedCallSummary
        """
        return _resource.unwrap(
            get_refused_call_summary.sync_detailed(
                client=self._client,
                days=days,
                from_=from_,
                to=to,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    def list_refused(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[RefusedCall]:
        """List refused calls

         Return the calls Talki refused before answering, newest first. Requires `calls:read`. Limited to 600
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of refused calls to return. Default: 50.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page.
            location_id (None | str | Unset): Only the refused calls of this location
                (`RefusedCall.location_id`), an id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Page[RefusedCall]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """

        def fetch(cursor: None | str | Unset) -> RefusedCallList:
            return _resource.unwrap(
                list_refused_calls.sync_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _pagination.Page.first(fetch, cursor)

    def mark_all_read(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> MarkAllReadResult:
        """Mark all calls read

         Mark every unread call in the inbox read. Each one sends `call.updated`. Requires `calls:write`.
        Limited to 120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
                id from `GET /v1/locations`. Omit for the calls of every location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            MarkAllReadResult
        """
        return _resource.unwrap(
            mark_all_calls_read.sync_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def update(
        self,
        call_id: str,
        *,
        body: CallUpdate,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Call:
        """Update a call's inbox state

         Mark a call read or unread, archive it or return it to the inbox. Archiving marks it read. Requires
        `calls:write`. Limited to 120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            call_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (CallUpdate): Inbox state for one call. Send `read`, `archived` or both.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Call
        """
        return _resource.unwrap(
            update_call.sync_detailed(
                client=self._client,
                call_id=call_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        sync: bool | Unset = False,
        created_after: datetime.datetime | None | Unset = UNSET,
        created_before: datetime.datetime | None | Unset = UNSET,
        status: InboxStatus | Unset = InboxStatus.ALL,
        phone: None | str | Unset = UNSET,
        contact_id: None | str | Unset = UNSET,
        q: None | str | Unset = UNSET,
        outcome: CallOutcome | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[Call]:
        """List calls

         Read the newest-first call log, or set `sync=true` for a resumable change feed. Search the log with
        `phone`, `contact_id`, `q` or `outcome`; they do not combine with `sync=true`. Requires
        `calls:read`. Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of calls to return. Default: 50.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page. A cursor works only in the mode that issued it (`sync=true` or the
                default list); a cursor from the other mode is refused.
            sync (bool | Unset): Switch to the CHANGE FEED: ordered by when each record was committed,
                not by when the call started, and resumable exactly like `GET /v1/appointments`. This is
                how a system keeping its own copy recovers from missed webhooks — store `next_cursor`,
                which is returned on the last page too, and drive the loop from `has_more`. Leave it off
                for the newest-first list a person reads. Default: False.
            created_after (datetime.datetime | None | Unset): Only calls recorded at or after this
                instant (RFC 3339 UTC). Inclusive: a call at exactly this instant is returned, so dedupe
                on `id`. Filters on `created_at`, not `started_at` (see `Call.created_at`). Use it for
                reporting windows, not as a sync watermark: a timestamp watermark can skip a call
                permanently. Use `sync=true` to resume a sync; the two cannot be combined.
            created_before (datetime.datetime | None | Unset): Only calls recorded strictly before
                this instant (RFC 3339 UTC).
            status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
                and not yet read. `archived` — archived calls. `all` — every call. Default:
                InboxStatus.ALL.
            phone (None | str | Unset): Only calls from this number: E.164, or a national number read
                as Italian. Not with `sync=true`.
            contact_id (None | str | Unset): Only calls from this contact's number
                (`caller.contact_id`). Not with `sync=true`.
            q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
                contains it, or whose caller's `display_name` does. A name that is not published as
                `display_name` is not searched either. Not with `sync=true`.
            outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
                `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
                outcomes were tracked have none and match no value. Not with `sync=true`.
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
            Page[Call]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """

        def fetch(cursor: None | str | Unset) -> CallList:
            return _resource.unwrap(
                list_calls.sync_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    sync=sync,
                    created_after=created_after,
                    created_before=created_before,
                    status=status,
                    phone=phone,
                    contact_id=contact_id,
                    q=q,
                    outcome=outcome,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _pagination.Page.first(fetch, cursor)


class AsyncCallsResource(_resource.Resource):
    """`talki.calls` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    async def count(
        self,
        *,
        status: InboxStatus | Unset = InboxStatus.ALL,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> CallCount:
        """Count calls

         Count the calls in one inbox view. `status=unread` is the unread badge. Requires `calls:read`.
        Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
                and not yet read. `archived` — archived calls. `all` — every call. Default:
                InboxStatus.ALL.
            location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
                id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallCount
        """
        return _resource.unwrap(
            await count_calls.asyncio_detailed(
                client=self._client,
                status=status,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    async def count_refused(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> CallCount:
        """Count refused calls

         Count every refused call the account has. Requires `calls:read`. Limited to 600 requests per minute
        per account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): Only the refused calls of this location
                (`RefusedCall.location_id`), an id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallCount
        """
        return _resource.unwrap(
            await count_refused_calls.asyncio_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    async def delete(
        self,
        call_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a call

         Delete a call for good, when the caller asks to be forgotten: the call, its transcript, the
        questions it left and the pending contacts it proposed. The appointments it booked stay, with
        `call_id` null. The talk time it used stays on the meter of `GET /v1/usage` and, for a partner-
        managed account, in the partner's usage report; `GET /v1/usage/history` and the call statistics no
        longer count the call. Sends `call.deleted`. Requires `calls:delete`. Limited to 120 requests per
        minute per account (API key) or per installation (OAuth).

        Args:
            call_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        _resource.unwrap(
            await delete_call.asyncio_detailed(
                client=self._client,
                call_id=call_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def export_call(
        self,
        call_id: str,
        *,
        format_: ExportFormat | Unset = ExportFormat.PDF,
        talki_version: str | Unset = UNSET,
    ) -> File:
        """Export a call

         Return one call as a PDF or Excel file, on every plan. It includes the conversation only with
        `transcripts:read` and when the account keeps transcripts, and the call's appointments only with
        `appointments:read`. Requires `calls:read`. Limited to 600 requests per minute per account (API key)
        or per installation (OAuth), and to 10 file exports per minute.

        Args:
            call_id (str):
            format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
                ExportFormat.PDF.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            File
        """
        return _resource.unwrap(
            await export_call.asyncio_detailed(
                client=self._client,
                call_id=call_id,
                format_=format_,
                talki_version=talki_version,
            )
        )

    async def export_calls(
        self,
        *,
        from_: datetime.date,
        to: datetime.date,
        format_: ExportFormat | Unset = ExportFormat.PDF,
        status: InboxStatus | Unset = InboxStatus.ALL,
        q: None | str | Unset = UNSET,
        outcome: CallOutcome | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> File:
        """Export the call log

         Return the calls of a date range as a PDF or Excel file, without transcripts. `status` defaults to
        `all`; `status`, `q` and `outcome` narrow the file as they narrow `GET /v1/calls`. Each call's
        appointments are included only when the credential also holds `appointments:read`. Needs a plan that
        includes the call log export. Requires `calls:read`. Limited to 600 requests per minute per account
        (API key) or per installation (OAuth), and to 10 file exports per minute.

        Args:
            from_ (datetime.date): First day, `YYYY-MM-DD`, local to the account's `timezone`.
            to (datetime.date): Last day, included, `YYYY-MM-DD`. At most 366 days after `from`.
            format_ (ExportFormat | Unset): `pdf` for a document, `xlsx` for an Excel sheet. Default:
                ExportFormat.PDF.
            status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
                and not yet read. `archived` — archived calls. `all` — every call. Default:
                InboxStatus.ALL.
            q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
                contains it, or whose caller's `display_name` does. A name that is not published as
                `display_name` is not searched either.
            outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
                `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
                outcomes were tracked have none and match no value.
            location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
                id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            File
        """
        return _resource.unwrap(
            await export_calls.asyncio_detailed(
                client=self._client,
                from_=from_,
                to=to,
                format_=format_,
                status=status,
                q=q,
                outcome=outcome,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    async def get(
        self,
        call_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Call:
        """Retrieve a call

         Return one call belonging to the authenticated account. Requires `calls:read`. Limited to 600
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            call_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Call
        """
        return _resource.unwrap(
            await get_call.asyncio_detailed(
                client=self._client,
                call_id=call_id,
                talki_version=talki_version,
            )
        )

    async def get_stats(
        self,
        *,
        days: int | None | Unset = UNSET,
        from_: datetime.date | None | Unset = UNSET,
        to: datetime.date | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> CallStats:
        """Retrieve call statistics

         Return totals, the daily series and the top callers over the last `days`, or over the local days
        `from` to `to` (at most 366). Requires `calls:read`. Limited to 600 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            days (int | None | Unset): Length of the period, in days, ending now. Default 30. Cannot
                be combined with `from` / `to`.
            from_ (datetime.date | None | Unset): First day of the period, `YYYY-MM-DD`, local to the
                account's `timezone`. Sent with `to`, instead of `days`.
            to (datetime.date | None | Unset): Last day of the period, included, `YYYY-MM-DD`. At most
                366 days after `from`.
            location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
                id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallStats
        """
        return _resource.unwrap(
            await get_call_stats.asyncio_detailed(
                client=self._client,
                days=days,
                from_=from_,
                to=to,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    async def get_transcript(
        self,
        call_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> CallTranscript:
        """Retrieve a call transcript

         Return the automatic transcript of one call. `calls:read` does not grant it: the account owner ticks
        `transcripts:read` on its own. Requires `transcripts:read`. Limited to 600 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            call_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallTranscript
        """
        return _resource.unwrap(
            await get_call_transcript.asyncio_detailed(
                client=self._client,
                call_id=call_id,
                talki_version=talki_version,
            )
        )

    async def get_refused_summary(
        self,
        *,
        days: int | None | Unset = UNSET,
        from_: datetime.date | None | Unset = UNSET,
        to: datetime.date | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> RefusedCallSummary:
        """Summarise refused calls

         Return refused calls over the last `days`, or over the local days `from` to `to`, by reason, and the
        actions they call for. Requires `calls:read`. Limited to 600 requests per minute per account (API
        key) or per installation (OAuth).

        Args:
            days (int | None | Unset): Length of the period, in days, ending now. Default 30. Cannot
                be combined with `from` / `to`.
            from_ (datetime.date | None | Unset): First day of the period, `YYYY-MM-DD`, local to the
                account's `timezone`. Sent with `to`, instead of `days`.
            to (datetime.date | None | Unset): Last day of the period, included, `YYYY-MM-DD`. At most
                366 days after `from`.
            location_id (None | str | Unset): Only the refused calls of this location
                (`RefusedCall.location_id`), an id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            RefusedCallSummary
        """
        return _resource.unwrap(
            await get_refused_call_summary.asyncio_detailed(
                client=self._client,
                days=days,
                from_=from_,
                to=to,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    async def list_refused(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPage[RefusedCall]:
        """List refused calls

         Return the calls Talki refused before answering, newest first. Requires `calls:read`. Limited to 600
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of refused calls to return. Default: 50.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page.
            location_id (None | str | Unset): Only the refused calls of this location
                (`RefusedCall.location_id`), an id from `GET /v1/locations`. Omit for every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AsyncPage[RefusedCall]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """

        async def fetch(cursor: None | str | Unset) -> RefusedCallList:
            return _resource.unwrap(
                await list_refused_calls.asyncio_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return await _pagination.AsyncPage.first(fetch, cursor)

    async def mark_all_read(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> MarkAllReadResult:
        """Mark all calls read

         Mark every unread call in the inbox read. Each one sends `call.updated`. Requires `calls:write`.
        Limited to 120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): Only the calls of this location (`Call.location_id`), an
                id from `GET /v1/locations`. Omit for the calls of every location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            MarkAllReadResult
        """
        return _resource.unwrap(
            await mark_all_calls_read.asyncio_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def update(
        self,
        call_id: str,
        *,
        body: CallUpdate,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Call:
        """Update a call's inbox state

         Mark a call read or unread, archive it or return it to the inbox. Archiving marks it read. Requires
        `calls:write`. Limited to 120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            call_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (CallUpdate): Inbox state for one call. Send `read`, `archived` or both.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Call
        """
        return _resource.unwrap(
            await update_call.asyncio_detailed(
                client=self._client,
                call_id=call_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        sync: bool | Unset = False,
        created_after: datetime.datetime | None | Unset = UNSET,
        created_before: datetime.datetime | None | Unset = UNSET,
        status: InboxStatus | Unset = InboxStatus.ALL,
        phone: None | str | Unset = UNSET,
        contact_id: None | str | Unset = UNSET,
        q: None | str | Unset = UNSET,
        outcome: CallOutcome | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPage[Call]:
        """List calls

         Read the newest-first call log, or set `sync=true` for a resumable change feed. Search the log with
        `phone`, `contact_id`, `q` or `outcome`; they do not combine with `sync=true`. Requires
        `calls:read`. Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of calls to return. Default: 50.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page. A cursor works only in the mode that issued it (`sync=true` or the
                default list); a cursor from the other mode is refused.
            sync (bool | Unset): Switch to the CHANGE FEED: ordered by when each record was committed,
                not by when the call started, and resumable exactly like `GET /v1/appointments`. This is
                how a system keeping its own copy recovers from missed webhooks — store `next_cursor`,
                which is returned on the last page too, and drive the loop from `has_more`. Leave it off
                for the newest-first list a person reads. Default: False.
            created_after (datetime.datetime | None | Unset): Only calls recorded at or after this
                instant (RFC 3339 UTC). Inclusive: a call at exactly this instant is returned, so dedupe
                on `id`. Filters on `created_at`, not `started_at` (see `Call.created_at`). Use it for
                reporting windows, not as a sync watermark: a timestamp watermark can skip a call
                permanently. Use `sync=true` to resume a sync; the two cannot be combined.
            created_before (datetime.datetime | None | Unset): Only calls recorded strictly before
                this instant (RFC 3339 UTC).
            status (InboxStatus | Unset): `inbox` — calls not archived. `unread` — calls not archived
                and not yet read. `archived` — archived calls. `all` — every call. Default:
                InboxStatus.ALL.
            phone (None | str | Unset): Only calls from this number: E.164, or a national number read
                as Italian. Not with `sync=true`.
            contact_id (None | str | Unset): Only calls from this contact's number
                (`caller.contact_id`). Not with `sync=true`.
            q (None | str | Unset): Search, 2 to 100 characters, ignoring case: calls whose `summary`
                contains it, or whose caller's `display_name` does. A name that is not published as
                `display_name` is not searched either. Not with `sync=true`.
            outcome (CallOutcome | None | Unset): Only calls with this `outcome`: `booked`,
                `rescheduled`, `cancelled`, `transferred`, `unresolved`, `info`. Calls recorded before
                outcomes were tracked have none and match no value. Not with `sync=true`.
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
            AsyncPage[Call]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """

        async def fetch(cursor: None | str | Unset) -> CallList:
            return _resource.unwrap(
                await list_calls.asyncio_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    sync=sync,
                    created_after=created_after,
                    created_before=created_before,
                    status=status,
                    phone=phone,
                    contact_id=contact_id,
                    q=q,
                    outcome=outcome,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return await _pagination.AsyncPage.first(fetch, cursor)
