"""The `working_hours` operations, one module each, and `WorkingHoursResource` / `AsyncWorkingHoursResource`,
which `Talki` and `AsyncTalki` expose as `working_hours`."""

from ... import _resource
from ...models.working_hours import WorkingHours
from ...models.working_hours_update import WorkingHoursUpdate
from ...types import UNSET, Unset
from . import (
    get_working_hours,
    replace_working_hours,
)

__all__ = ["AsyncWorkingHoursResource", "WorkingHoursResource"]


class WorkingHoursResource(_resource.Resource):
    """`talki.working_hours`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

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
        return _resource.unwrap(
            get_working_hours.sync_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    def replace(
        self,
        *,
        body: WorkingHoursUpdate,
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
        return _resource.unwrap(
            replace_working_hours.sync_detailed(
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
        return _resource.unwrap(
            await get_working_hours.asyncio_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    async def replace(
        self,
        *,
        body: WorkingHoursUpdate,
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
        return _resource.unwrap(
            await replace_working_hours.asyncio_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
                if_match=if_match,
            )
        )
