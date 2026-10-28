"""The `availability` operations, one module each, and `AvailabilityResource` / `AsyncAvailabilityResource`,
which `Talki` and `AsyncTalki` expose as `availability`."""

import datetime
from functools import cached_property

from ... import _resource
from ...models.availability import Availability
from ...types import UNSET, Unset
from . import (
    get_availability,
)

__all__ = [
    "AsyncAvailabilityResource",
    "AsyncAvailabilityResourceWithRawResponse",
    "AvailabilityResource",
    "AvailabilityResourceWithRawResponse",
]


class AvailabilityResourceWithRawResponse(_resource.Resource):
    """`talki.availability.with_raw_response`: the methods of `talki.availability`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def get(
        self,
        *,
        service_id: str,
        from_: datetime.date,
        to: datetime.date,
        quantity: int | Unset = 1,
        stay_length: int | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Availability]:
        """`talki.availability.get`, returning the whole answer."""
        return _resource.raw(
            get_availability.sync_detailed(
                client=self._client,
                service_id=service_id,
                from_=from_,
                to=to,
                quantity=quantity,
                stay_length=stay_length,
                talki_version=talki_version,
            )
        )


class AvailabilityResource(_resource.Resource):
    """`talki.availability`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AvailabilityResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AvailabilityResourceWithRawResponse(self._client)

    def get(
        self,
        *,
        service_id: str,
        from_: datetime.date,
        to: datetime.date,
        quantity: int | Unset = 1,
        stay_length: int | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> Availability:
        """Retrieve availability

         Return advisory bookable windows for one service and local date range. Requires `availability:read`.
        Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            service_id (str): The service to check. Required. Availability is per service: two
                services that share a resource can return different windows.
            from_ (datetime.date): First local date to report, `YYYY-MM-DD`, in the account's
                timezone. Inclusive.
            to (datetime.date): Last local date to report, `YYYY-MM-DD`. Inclusive, so `from` equal to
                `to` asks about one day. At most 62 days per request.
            quantity (int | Unset): Party size, for a service that asks for one (`asks_quantity` on
                `GET /v1/services`). Pass the party size you intend to book: the windows depend on it.
                Ignored, and forced to 1, for a service that does not ask. Outside the service's
                `min_quantity`/`max_quantity` it is refused with 400 `invalid_parameter`, as the booking
                would be. Default: 1.
            stay_length (int | None | Unset): Length of the stay, in the service's `range_unit`
                (nights or days). **Required for a `day_range` service and rejected for any other.** Each
                date in the range then answers whether a stay of this length can begin on it.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Availability
        """
        return (
            self.with_raw_response.get(
                service_id=service_id,
                from_=from_,
                to=to,
                quantity=quantity,
                stay_length=stay_length,
                talki_version=talki_version,
            )
        ).parse()


class AsyncAvailabilityResourceWithRawResponse(_resource.Resource):
    """`talki.availability.with_raw_response` on `AsyncTalki`: the methods of `talki.availability`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def get(
        self,
        *,
        service_id: str,
        from_: datetime.date,
        to: datetime.date,
        quantity: int | Unset = 1,
        stay_length: int | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Availability]:
        """`talki.availability.get`, returning the whole answer."""
        return _resource.raw(
            await get_availability.asyncio_detailed(
                client=self._client,
                service_id=service_id,
                from_=from_,
                to=to,
                quantity=quantity,
                stay_length=stay_length,
                talki_version=talki_version,
            )
        )


class AsyncAvailabilityResource(_resource.Resource):
    """`talki.availability` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncAvailabilityResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncAvailabilityResourceWithRawResponse(self._client)

    async def get(
        self,
        *,
        service_id: str,
        from_: datetime.date,
        to: datetime.date,
        quantity: int | Unset = 1,
        stay_length: int | None | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> Availability:
        """Retrieve availability

         Return advisory bookable windows for one service and local date range. Requires `availability:read`.
        Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            service_id (str): The service to check. Required. Availability is per service: two
                services that share a resource can return different windows.
            from_ (datetime.date): First local date to report, `YYYY-MM-DD`, in the account's
                timezone. Inclusive.
            to (datetime.date): Last local date to report, `YYYY-MM-DD`. Inclusive, so `from` equal to
                `to` asks about one day. At most 62 days per request.
            quantity (int | Unset): Party size, for a service that asks for one (`asks_quantity` on
                `GET /v1/services`). Pass the party size you intend to book: the windows depend on it.
                Ignored, and forced to 1, for a service that does not ask. Outside the service's
                `min_quantity`/`max_quantity` it is refused with 400 `invalid_parameter`, as the booking
                would be. Default: 1.
            stay_length (int | None | Unset): Length of the stay, in the service's `range_unit`
                (nights or days). **Required for a `day_range` service and rejected for any other.** Each
                date in the range then answers whether a stay of this length can begin on it.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Availability
        """
        return (
            await self.with_raw_response.get(
                service_id=service_id,
                from_=from_,
                to=to,
                quantity=quantity,
                stay_length=stay_length,
                talki_version=talki_version,
            )
        ).parse()
