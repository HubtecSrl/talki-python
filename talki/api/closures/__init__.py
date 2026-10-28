"""The `closures` operations, one module each, and `ClosuresResource` / `AsyncClosuresResource`,
which `Talki` and `AsyncTalki` expose as `closures`."""

import datetime
from functools import cached_property

from ... import _resource
from ...models.closure import Closure
from ...models.closure_create import ClosureCreate, ClosureCreateDict
from ...models.closure_list import ClosureList
from ...models.closure_update import ClosureUpdate, ClosureUpdateDict
from ...models.list_closures_kind import ListClosuresKind
from ...types import UNSET, Unset
from . import (
    create_closure,
    delete_closure,
    list_closures,
    update_closure,
)

__all__ = [
    "AsyncClosuresResource",
    "AsyncClosuresResourceWithRawResponse",
    "ClosuresResource",
    "ClosuresResourceWithRawResponse",
]


class ClosuresResourceWithRawResponse(_resource.Resource):
    """`talki.closures.with_raw_response`: the methods of `talki.closures`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def create(
        self,
        *,
        body: ClosureCreate | ClosureCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Closure]:
        """`talki.closures.create`, returning the whole answer."""
        body = _resource.as_body(body, ClosureCreate)
        return _resource.raw(
            create_closure.sync_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def delete(
        self,
        closure_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.closures.delete`, returning the whole answer."""
        return _resource.raw(
            delete_closure.sync_detailed(
                client=self._client,
                closure_id=closure_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def update(
        self,
        closure_id: str,
        *,
        body: ClosureUpdate | ClosureUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Closure]:
        """`talki.closures.update`, returning the whole answer."""
        body = _resource.as_body(body, ClosureUpdate)
        return _resource.raw(
            update_closure.sync_detailed(
                client=self._client,
                closure_id=closure_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def list(
        self,
        *,
        from_: datetime.date | None | Unset = UNSET,
        to: datetime.date | None | Unset = UNSET,
        kind: ListClosuresKind | Unset = ListClosuresKind.CLOSED,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[ClosureList]:
        """`talki.closures.list`, returning the whole answer."""
        return _resource.raw(
            list_closures.sync_detailed(
                client=self._client,
                from_=from_,
                to=to,
                kind=kind,
                location_id=location_id,
                talki_version=talki_version,
            )
        )


class ClosuresResource(_resource.Resource):
    """`talki.closures`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> ClosuresResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return ClosuresResourceWithRawResponse(self._client)

    def create(
        self,
        *,
        body: ClosureCreate | ClosureCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Closure:
        """Create a closure

         Close whole days or an exact range, or add hours to one day with a special opening, which must start
        and end on the same day: at the location `location_id` names, or at every location without it.
        Appointments already inside a closure are not cancelled. Requires `Idempotency-Key`. Requires
        `account:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (ClosureCreate | ClosureCreateDict): A new closure or special opening: `all_day: true` with `start_date`
                and `end_date` (closures only), or an exact range with `start_at` and `end_at`. Sending
                fields of both forms is refused, and so is a special opening that does not start and end
                on the same day in the account's `timezone`. Without `location_id`, it applies at every
                location.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Closure
        """
        return (
            self.with_raw_response.create(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def delete(
        self,
        closure_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a closure

         Remove a closure or special opening. The time it covered follows the weekly hours again. Requires
        `account:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            closure_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            self.with_raw_response.delete(
                closure_id=closure_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def update(
        self,
        closure_id: str,
        *,
        body: ClosureUpdate | ClosureUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Closure:
        """Update a closure

         Change a closure or special opening; omitted fields stay unchanged. To move it, send the whole new
        window. A special opening must still start and end on the same day. Its `location_id` cannot change.
        A request that changes nothing sends no `closure.updated`. Requires `account:write`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            closure_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (ClosureUpdate | ClosureUpdateDict): A partial edit of a closure or special opening. To move it, send the
                whole new window in one of the two forms. It stays at the location it was created for.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Closure
        """
        return (
            self.with_raw_response.update(
                closure_id=closure_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list(
        self,
        *,
        from_: datetime.date | None | Unset = UNSET,
        to: datetime.date | None | Unset = UNSET,
        kind: ListClosuresKind | Unset = ListClosuresKind.CLOSED,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> ClosureList:
        """List closures

         Return the closures, special openings or both overlapping a range of local days, earliest first, in
        one page. Closures only unless `kind` says otherwise. With `location_id`, only those that apply at
        that location, including those of every location. Requires `account:read`. Limited to 600 requests
        per minute per account (API key) or per installation (OAuth).

        Args:
            from_ (datetime.date | None | Unset): First day to list, `YYYY-MM-DD`. Defaults to today.
            to (datetime.date | None | Unset): Last day to list, included, `YYYY-MM-DD`. Defaults to a
                year after `from`. At most 366 days after `from`.
            kind (ListClosuresKind | Unset): `closed` (the default) for closures, `open` for special
                openings, `all` for both. Default: ListClosuresKind.CLOSED.
            location_id (None | str | Unset): Only those that apply at this location, an id from `GET
                /v1/locations`: its own, and those of every location (`location_id` null). Omit for every
                closure of every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            ClosureList
        """
        return (
            self.with_raw_response.list(
                from_=from_,
                to=to,
                kind=kind,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()


class AsyncClosuresResourceWithRawResponse(_resource.Resource):
    """`talki.closures.with_raw_response` on `AsyncTalki`: the methods of `talki.closures`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def create(
        self,
        *,
        body: ClosureCreate | ClosureCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Closure]:
        """`talki.closures.create`, returning the whole answer."""
        body = _resource.as_body(body, ClosureCreate)
        return _resource.raw(
            await create_closure.asyncio_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def delete(
        self,
        closure_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.closures.delete`, returning the whole answer."""
        return _resource.raw(
            await delete_closure.asyncio_detailed(
                client=self._client,
                closure_id=closure_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def update(
        self,
        closure_id: str,
        *,
        body: ClosureUpdate | ClosureUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Closure]:
        """`talki.closures.update`, returning the whole answer."""
        body = _resource.as_body(body, ClosureUpdate)
        return _resource.raw(
            await update_closure.asyncio_detailed(
                client=self._client,
                closure_id=closure_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def list(
        self,
        *,
        from_: datetime.date | None | Unset = UNSET,
        to: datetime.date | None | Unset = UNSET,
        kind: ListClosuresKind | Unset = ListClosuresKind.CLOSED,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[ClosureList]:
        """`talki.closures.list`, returning the whole answer."""
        return _resource.raw(
            await list_closures.asyncio_detailed(
                client=self._client,
                from_=from_,
                to=to,
                kind=kind,
                location_id=location_id,
                talki_version=talki_version,
            )
        )


class AsyncClosuresResource(_resource.Resource):
    """`talki.closures` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncClosuresResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncClosuresResourceWithRawResponse(self._client)

    async def create(
        self,
        *,
        body: ClosureCreate | ClosureCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Closure:
        """Create a closure

         Close whole days or an exact range, or add hours to one day with a special opening, which must start
        and end on the same day: at the location `location_id` names, or at every location without it.
        Appointments already inside a closure are not cancelled. Requires `Idempotency-Key`. Requires
        `account:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (ClosureCreate | ClosureCreateDict): A new closure or special opening: `all_day: true` with `start_date`
                and `end_date` (closures only), or an exact range with `start_at` and `end_at`. Sending
                fields of both forms is refused, and so is a special opening that does not start and end
                on the same day in the account's `timezone`. Without `location_id`, it applies at every
                location.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Closure
        """
        return (
            await self.with_raw_response.create(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def delete(
        self,
        closure_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a closure

         Remove a closure or special opening. The time it covered follows the weekly hours again. Requires
        `account:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            closure_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            await self.with_raw_response.delete(
                closure_id=closure_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def update(
        self,
        closure_id: str,
        *,
        body: ClosureUpdate | ClosureUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Closure:
        """Update a closure

         Change a closure or special opening; omitted fields stay unchanged. To move it, send the whole new
        window. A special opening must still start and end on the same day. Its `location_id` cannot change.
        A request that changes nothing sends no `closure.updated`. Requires `account:write`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            closure_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (ClosureUpdate | ClosureUpdateDict): A partial edit of a closure or special opening. To move it, send the
                whole new window in one of the two forms. It stays at the location it was created for.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Closure
        """
        return (
            await self.with_raw_response.update(
                closure_id=closure_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def list(
        self,
        *,
        from_: datetime.date | None | Unset = UNSET,
        to: datetime.date | None | Unset = UNSET,
        kind: ListClosuresKind | Unset = ListClosuresKind.CLOSED,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> ClosureList:
        """List closures

         Return the closures, special openings or both overlapping a range of local days, earliest first, in
        one page. Closures only unless `kind` says otherwise. With `location_id`, only those that apply at
        that location, including those of every location. Requires `account:read`. Limited to 600 requests
        per minute per account (API key) or per installation (OAuth).

        Args:
            from_ (datetime.date | None | Unset): First day to list, `YYYY-MM-DD`. Defaults to today.
            to (datetime.date | None | Unset): Last day to list, included, `YYYY-MM-DD`. Defaults to a
                year after `from`. At most 366 days after `from`.
            kind (ListClosuresKind | Unset): `closed` (the default) for closures, `open` for special
                openings, `all` for both. Default: ListClosuresKind.CLOSED.
            location_id (None | str | Unset): Only those that apply at this location, an id from `GET
                /v1/locations`: its own, and those of every location (`location_id` null). Omit for every
                closure of every location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            ClosureList
        """
        return (
            await self.with_raw_response.list(
                from_=from_,
                to=to,
                kind=kind,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()
