"""The `working_hours` operations, one module each, and `WorkingHoursResource` / `AsyncWorkingHoursResource`,
which `Talki` and `AsyncTalki` expose as `working_hours`."""

from functools import cached_property

from ... import _resource
from ...models.working_hours import WorkingHours
from ...models.working_hours_update import WorkingHoursUpdate, WorkingHoursUpdateDict
from ...types import UNSET, Unset
from . import (
    get_working_hours,
    replace_working_hours,
)

__all__ = [
    "AsyncWorkingHoursResource",
    "AsyncWorkingHoursResourceWithRawResponse",
    "WorkingHoursResource",
    "WorkingHoursResourceWithRawResponse",
]


class WorkingHoursResourceWithRawResponse(_resource.Resource):
    """`talki.working_hours.with_raw_response`: the methods of `talki.working_hours`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[WorkingHours]:
        """`talki.working_hours.get`, returning the whole answer."""
        return _resource.raw(
            get_working_hours.sync_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    def replace(
        self,
        *,
        body: WorkingHoursUpdate | WorkingHoursUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
        if_match: str | Unset = UNSET,
    ) -> _resource.RawResponse[WorkingHours]:
        """`talki.working_hours.replace`, returning the whole answer."""
        body = _resource.as_body(body, WorkingHoursUpdate)
        return _resource.raw(
            replace_working_hours.sync_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
                if_match=if_match,
            )
        )


class WorkingHoursResource(_resource.Resource):
    """`talki.working_hours`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> WorkingHoursResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return WorkingHoursResourceWithRawResponse(self._client)

    def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> WorkingHours:
        """Retrieve working hours

         Return one location's weekly opening hours, the main location's unless `location_id` names another,
        with an `ETag` to send back as `If-Match`. Requires `account:read`. Limited to 600 requests per
        minute per account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): The location whose weekly hours to read, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WorkingHours
        """
        return (
            self.with_raw_response.get(
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()

    def replace(
        self,
        *,
        body: WorkingHoursUpdate | WorkingHoursUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
        if_match: str | Unset = UNSET,
    ) -> WorkingHours:
        """Replace working hours

         Replace one location's whole weekly schedule, the main location's unless `location_id` names
        another. `GET /v1/availability` and the assistant use the new hours at once. Requires
        `account:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            location_id (None | str | Unset): The location whose weekly hours to replace, an id from
                `GET /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            if_match (str | Unset):
            body (WorkingHoursUpdate): The whole week, replacing the current schedule. A slot you
                leave out is an opening removed, so read the hours first and send them back changed.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WorkingHours
        """
        return (
            self.with_raw_response.replace(
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
                if_match=if_match,
            )
        ).parse()


class AsyncWorkingHoursResourceWithRawResponse(_resource.Resource):
    """`talki.working_hours.with_raw_response` on `AsyncTalki`: the methods of `talki.working_hours`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[WorkingHours]:
        """`talki.working_hours.get`, returning the whole answer."""
        return _resource.raw(
            await get_working_hours.asyncio_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    async def replace(
        self,
        *,
        body: WorkingHoursUpdate | WorkingHoursUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
        if_match: str | Unset = UNSET,
    ) -> _resource.RawResponse[WorkingHours]:
        """`talki.working_hours.replace`, returning the whole answer."""
        body = _resource.as_body(body, WorkingHoursUpdate)
        return _resource.raw(
            await replace_working_hours.asyncio_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
                if_match=if_match,
            )
        )


class AsyncWorkingHoursResource(_resource.Resource):
    """`talki.working_hours` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncWorkingHoursResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncWorkingHoursResourceWithRawResponse(self._client)

    async def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> WorkingHours:
        """Retrieve working hours

         Return one location's weekly opening hours, the main location's unless `location_id` names another,
        with an `ETag` to send back as `If-Match`. Requires `account:read`. Limited to 600 requests per
        minute per account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): The location whose weekly hours to read, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WorkingHours
        """
        return (
            await self.with_raw_response.get(
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()

    async def replace(
        self,
        *,
        body: WorkingHoursUpdate | WorkingHoursUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
        if_match: str | Unset = UNSET,
    ) -> WorkingHours:
        """Replace working hours

         Replace one location's whole weekly schedule, the main location's unless `location_id` names
        another. `GET /v1/availability` and the assistant use the new hours at once. Requires
        `account:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            location_id (None | str | Unset): The location whose weekly hours to replace, an id from
                `GET /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            if_match (str | Unset):
            body (WorkingHoursUpdate): The whole week, replacing the current schedule. A slot you
                leave out is an opening removed, so read the hours first and send them back changed.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WorkingHours
        """
        return (
            await self.with_raw_response.replace(
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
                if_match=if_match,
            )
        ).parse()
