"""The `unresolved_requests` operations, one module each, and `UnresolvedRequestsResource` / `AsyncUnresolvedRequestsResource`,
which `Talki` and `AsyncTalki` expose as `unresolved_requests`."""

from functools import cached_property

from ... import _resource
from ... import pagination as _pagination
from ...models.unresolved_request import UnresolvedRequest
from ...models.unresolved_request_list import UnresolvedRequestList
from ...models.unresolved_request_status import UnresolvedRequestStatus
from ...models.unresolved_request_teach import UnresolvedRequestTeach, UnresolvedRequestTeachDict
from ...models.unresolved_request_teaching import UnresolvedRequestTeaching
from ...models.unresolved_request_update import UnresolvedRequestUpdate, UnresolvedRequestUpdateDict
from ...types import UNSET, Unset
from . import (
    get_unresolved_request,
    list_unresolved_requests,
    teach_unresolved_request,
    update_unresolved_request,
)

__all__ = [
    "AsyncUnresolvedRequestsResource",
    "AsyncUnresolvedRequestsResourceWithRawResponse",
    "UnresolvedRequestsResource",
    "UnresolvedRequestsResourceWithRawResponse",
]


class UnresolvedRequestsResourceWithRawResponse(_resource.Resource):
    """`talki.unresolved_requests.with_raw_response`: the methods of `talki.unresolved_requests`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def get(
        self,
        request_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[UnresolvedRequest]:
        """`talki.unresolved_requests.get`, returning the whole answer."""
        return _resource.raw(
            get_unresolved_request.sync_detailed(
                client=self._client,
                request_id=request_id,
                talki_version=talki_version,
            )
        )

    def teach(
        self,
        request_id: str,
        *,
        body: UnresolvedRequestTeach | UnresolvedRequestTeachDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[UnresolvedRequestTeaching]:
        """`talki.unresolved_requests.teach`, returning the whole answer."""
        body = _resource.as_body(body, UnresolvedRequestTeach)
        return _resource.raw(
            teach_unresolved_request.sync_detailed(
                client=self._client,
                request_id=request_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def update(
        self,
        request_id: str,
        *,
        body: UnresolvedRequestUpdate | UnresolvedRequestUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[UnresolvedRequest]:
        """`talki.unresolved_requests.update`, returning the whole answer."""
        body = _resource.as_body(body, UnresolvedRequestUpdate)
        return _resource.raw(
            update_unresolved_request.sync_detailed(
                client=self._client,
                request_id=request_id,
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
        status: None | UnresolvedRequestStatus | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.Page[UnresolvedRequest]]:
        """`talki.unresolved_requests.list`, returning the whole answer."""

        def fetch(cursor: None | str | Unset) -> UnresolvedRequestList:
            return _resource.unwrap(
                list_unresolved_requests.sync_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    status=status,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            list_unresolved_requests.sync_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                status=status,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.Page(page, fetch, cursor))


class UnresolvedRequestsResource(_resource.Resource):
    """`talki.unresolved_requests`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> UnresolvedRequestsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return UnresolvedRequestsResourceWithRawResponse(self._client)

    def get(
        self,
        request_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> UnresolvedRequest:
        """Retrieve an unresolved request

         Return one unresolved request belonging to the account. Requires `unresolved:read`. Limited to 600
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            request_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            UnresolvedRequest
        """
        return (
            self.with_raw_response.get(
                request_id=request_id,
                talki_version=talki_version,
            )
        ).parse()

    def teach(
        self,
        request_id: str,
        *,
        body: UnresolvedRequestTeach | UnresolvedRequestTeachDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> UnresolvedRequestTeaching:
        """Teach the assistant an answer

         Add the general answer to a resolved request's question to a FAQ note the assistant uses with every
        caller: the request's location's, another location's, or every location's (`all`). The business
        sees, rewords and removes it in Talki, and nothing asks for its approval first, so agree with the
        business what to teach. The assistant uses the answer shortly after the `202`, once the note is
        indexed. Teaching the same request again adds another entry. Refused for a request that is not
        `resolved` (`unresolved_request_not_resolved`), when the note is full (`faq_full`) and when the
        account's knowledge storage is full (`payload_too_large`). Requires `Idempotency-Key`. Requires
        `knowledge:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            request_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (UnresolvedRequestTeach | UnresolvedRequestTeachDict): The general answer to a resolved request's question,
                written as the business would say it to any caller. It is added to a FAQ note the business
                sees and edits in Talki. It is not the request's `answer`, which records what one caller
                was told, and does not change it.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            UnresolvedRequestTeaching
        """
        return (
            self.with_raw_response.teach(
                request_id=request_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def update(
        self,
        request_id: str,
        *,
        body: UnresolvedRequestUpdate | UnresolvedRequestUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> UnresolvedRequest:
        """Update an unresolved request

         Resolve, dismiss or reopen a request, or note the answer given to the caller. Requires
        `unresolved:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            request_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (UnresolvedRequestUpdate | UnresolvedRequestUpdateDict): A new status for an unresolved request, the answer given
                to the caller, or both. Send at least one.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            UnresolvedRequest
        """
        return (
            self.with_raw_response.update(
                request_id=request_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        status: None | UnresolvedRequestStatus | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[UnresolvedRequest]:
        """List unresolved-request changes

         Walk the feed of questions the assistant could not answer. A request moves again when it is closed.
        Requires `unresolved:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of requests to return. Default: 50.
            cursor (None | str | Unset): Opaque position in the change feed, from a previous
                response's `next_cursor`. Omit to start from the beginning. Not interchangeable with
                another endpoint's cursor.
            status (None | UnresolvedRequestStatus | Unset): Restrict to `open`, `resolved` or
                `dismissed`. Omit to get all of them — which is what an incremental sync needs, since a
                request being closed is the change you most need to see. Use this only for a point-in-time
                snapshot of the open list.
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
            Page[UnresolvedRequest]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """
        return (
            self.with_raw_response.list(
                limit=limit,
                cursor=cursor,
                status=status,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()


class AsyncUnresolvedRequestsResourceWithRawResponse(_resource.Resource):
    """`talki.unresolved_requests.with_raw_response` on `AsyncTalki`: the methods of `talki.unresolved_requests`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def get(
        self,
        request_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[UnresolvedRequest]:
        """`talki.unresolved_requests.get`, returning the whole answer."""
        return _resource.raw(
            await get_unresolved_request.asyncio_detailed(
                client=self._client,
                request_id=request_id,
                talki_version=talki_version,
            )
        )

    async def teach(
        self,
        request_id: str,
        *,
        body: UnresolvedRequestTeach | UnresolvedRequestTeachDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[UnresolvedRequestTeaching]:
        """`talki.unresolved_requests.teach`, returning the whole answer."""
        body = _resource.as_body(body, UnresolvedRequestTeach)
        return _resource.raw(
            await teach_unresolved_request.asyncio_detailed(
                client=self._client,
                request_id=request_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def update(
        self,
        request_id: str,
        *,
        body: UnresolvedRequestUpdate | UnresolvedRequestUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[UnresolvedRequest]:
        """`talki.unresolved_requests.update`, returning the whole answer."""
        body = _resource.as_body(body, UnresolvedRequestUpdate)
        return _resource.raw(
            await update_unresolved_request.asyncio_detailed(
                client=self._client,
                request_id=request_id,
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
        status: None | UnresolvedRequestStatus | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.AsyncPage[UnresolvedRequest]]:
        """`talki.unresolved_requests.list`, returning the whole answer."""

        async def fetch(cursor: None | str | Unset) -> UnresolvedRequestList:
            return _resource.unwrap(
                await list_unresolved_requests.asyncio_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    status=status,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            await list_unresolved_requests.asyncio_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                status=status,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.AsyncPage(page, fetch, cursor))


class AsyncUnresolvedRequestsResource(_resource.Resource):
    """`talki.unresolved_requests` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncUnresolvedRequestsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncUnresolvedRequestsResourceWithRawResponse(self._client)

    async def get(
        self,
        request_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> UnresolvedRequest:
        """Retrieve an unresolved request

         Return one unresolved request belonging to the account. Requires `unresolved:read`. Limited to 600
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            request_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            UnresolvedRequest
        """
        return (
            await self.with_raw_response.get(
                request_id=request_id,
                talki_version=talki_version,
            )
        ).parse()

    async def teach(
        self,
        request_id: str,
        *,
        body: UnresolvedRequestTeach | UnresolvedRequestTeachDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> UnresolvedRequestTeaching:
        """Teach the assistant an answer

         Add the general answer to a resolved request's question to a FAQ note the assistant uses with every
        caller: the request's location's, another location's, or every location's (`all`). The business
        sees, rewords and removes it in Talki, and nothing asks for its approval first, so agree with the
        business what to teach. The assistant uses the answer shortly after the `202`, once the note is
        indexed. Teaching the same request again adds another entry. Refused for a request that is not
        `resolved` (`unresolved_request_not_resolved`), when the note is full (`faq_full`) and when the
        account's knowledge storage is full (`payload_too_large`). Requires `Idempotency-Key`. Requires
        `knowledge:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            request_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (UnresolvedRequestTeach | UnresolvedRequestTeachDict): The general answer to a resolved request's question,
                written as the business would say it to any caller. It is added to a FAQ note the business
                sees and edits in Talki. It is not the request's `answer`, which records what one caller
                was told, and does not change it.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            UnresolvedRequestTeaching
        """
        return (
            await self.with_raw_response.teach(
                request_id=request_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def update(
        self,
        request_id: str,
        *,
        body: UnresolvedRequestUpdate | UnresolvedRequestUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> UnresolvedRequest:
        """Update an unresolved request

         Resolve, dismiss or reopen a request, or note the answer given to the caller. Requires
        `unresolved:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            request_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (UnresolvedRequestUpdate | UnresolvedRequestUpdateDict): A new status for an unresolved request, the answer given
                to the caller, or both. Send at least one.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            UnresolvedRequest
        """
        return (
            await self.with_raw_response.update(
                request_id=request_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        status: None | UnresolvedRequestStatus | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPager[UnresolvedRequest]:
        """List unresolved-request changes

         Walk the feed of questions the assistant could not answer. A request moves again when it is closed.
        Requires `unresolved:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of requests to return. Default: 50.
            cursor (None | str | Unset): Opaque position in the change feed, from a previous
                response's `next_cursor`. Omit to start from the beginning. Not interchangeable with
                another endpoint's cursor.
            status (None | UnresolvedRequestStatus | Unset): Restrict to `open`, `resolved` or
                `dismissed`. Omit to get all of them — which is what an incremental sync needs, since a
                request being closed is the change you most need to see. Use this only for a point-in-time
                snapshot of the open list.
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
            AsyncPager[UnresolvedRequest]: Awaited, this page (an `AsyncPage`). Iterated with `async for`,
            every row from here on, fetching the pages as it goes.
        """

        async def first() -> _pagination.AsyncPage[UnresolvedRequest]:
            return (
                await self.with_raw_response.list(
                    limit=limit,
                    cursor=cursor,
                    status=status,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            ).parse()

        return _pagination.AsyncPager(first)
