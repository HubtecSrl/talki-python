"""The `locations` operations, one module each, and `LocationsResource` / `AsyncLocationsResource`,
which `Talki` and `AsyncTalki` expose as `locations`."""

from functools import cached_property

from ... import _resource
from ...models.location_list import LocationList
from ...types import UNSET, Unset
from . import (
    list_locations,
)

__all__ = [
    "AsyncLocationsResource",
    "AsyncLocationsResourceWithRawResponse",
    "LocationsResource",
    "LocationsResourceWithRawResponse",
]


class LocationsResourceWithRawResponse(_resource.Resource):
    """`talki.locations.with_raw_response`: the methods of `talki.locations`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[LocationList]:
        """`talki.locations.list`, returning the whole answer."""
        return _resource.raw(
            list_locations.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class LocationsResource(_resource.Resource):
    """`talki.locations`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> LocationsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return LocationsResourceWithRawResponse(self._client)

    def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> LocationList:
        """List locations

         Return every location of the account in one page: the main one, any other, and inactive ones, which
        keep their records. An account whose `multi_sede` is false has exactly one, the main location.
        Resolve the `location_id` on calls, bookings, services, resources, unresolved requests and closures
        here. Requires `account:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            LocationList
        """
        return (
            self.with_raw_response.list(
                talki_version=talki_version,
            )
        ).parse()


class AsyncLocationsResourceWithRawResponse(_resource.Resource):
    """`talki.locations.with_raw_response` on `AsyncTalki`: the methods of `talki.locations`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[LocationList]:
        """`talki.locations.list`, returning the whole answer."""
        return _resource.raw(
            await list_locations.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class AsyncLocationsResource(_resource.Resource):
    """`talki.locations` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncLocationsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncLocationsResourceWithRawResponse(self._client)

    async def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> LocationList:
        """List locations

         Return every location of the account in one page: the main one, any other, and inactive ones, which
        keep their records. An account whose `multi_sede` is false has exactly one, the main location.
        Resolve the `location_id` on calls, bookings, services, resources, unresolved requests and closures
        here. Requires `account:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            LocationList
        """
        return (
            await self.with_raw_response.list(
                talki_version=talki_version,
            )
        ).parse()
