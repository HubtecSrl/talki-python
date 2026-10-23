"""The `locations` operations, one module each, and `LocationsResource` / `AsyncLocationsResource`,
which `Talki` and `AsyncTalki` expose as `locations`."""

from ... import _resource
from ...models.location_list import LocationList
from ...types import UNSET, Unset
from . import (
    list_locations,
)

__all__ = ["AsyncLocationsResource", "LocationsResource"]


class LocationsResource(_resource.Resource):
    """`talki.locations`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

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
        return _resource.unwrap(
            list_locations.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class AsyncLocationsResource(_resource.Resource):
    """`talki.locations` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

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
        return _resource.unwrap(
            await list_locations.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )
