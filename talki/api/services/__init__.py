"""The `services` operations, one module each, and `ServicesResource` / `AsyncServicesResource`,
which `Talki` and `AsyncTalki` expose as `services`."""

from functools import cached_property

from ... import _resource
from ... import pagination as _pagination
from ...models.service import Service
from ...models.service_create import ServiceCreate, ServiceCreateDict
from ...models.service_list import ServiceList
from ...models.service_update import ServiceUpdate, ServiceUpdateDict
from ...types import UNSET, Unset
from . import (
    create_service,
    delete_service,
    get_service,
    list_services,
    update_service,
)

__all__ = [
    "AsyncServicesResource",
    "AsyncServicesResourceWithRawResponse",
    "ServicesResource",
    "ServicesResourceWithRawResponse",
]


class ServicesResourceWithRawResponse(_resource.Resource):
    """`talki.services.with_raw_response`: the methods of `talki.services`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def create(
        self,
        *,
        body: ServiceCreate | ServiceCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Service]:
        """`talki.services.create`, returning the whole answer."""
        body = _resource.as_body(body, ServiceCreate)
        return _resource.raw(
            create_service.sync_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def delete(
        self,
        service_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.services.delete`, returning the whole answer."""
        return _resource.raw(
            delete_service.sync_detailed(
                client=self._client,
                service_id=service_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def get(
        self,
        service_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Service]:
        """`talki.services.get`, returning the whole answer."""
        return _resource.raw(
            get_service.sync_detailed(
                client=self._client,
                service_id=service_id,
                talki_version=talki_version,
            )
        )

    def update(
        self,
        service_id: str,
        *,
        body: ServiceUpdate | ServiceUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Service]:
        """`talki.services.update`, returning the whole answer."""
        body = _resource.as_body(body, ServiceUpdate)
        return _resource.raw(
            update_service.sync_detailed(
                client=self._client,
                service_id=service_id,
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
        is_active: bool | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.Page[Service]]:
        """`talki.services.list`, returning the whole answer."""

        def fetch(cursor: None | str | Unset) -> ServiceList:
            return _resource.unwrap(
                list_services.sync_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    is_active=is_active,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            list_services.sync_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                is_active=is_active,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.Page(page, fetch, cursor))


class ServicesResource(_resource.Resource):
    """`talki.services`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> ServicesResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return ServicesResourceWithRawResponse(self._client)

    def create(
        self,
        *,
        body: ServiceCreate | ServiceCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Service:
        """Create a service

         Create a service with a fixed duration, bookable at once, at the location `location_id` names, the
        main location without it. Send at most one of `initial_capacity` or `resource_ids` (resources of the
        same location); with neither, it draws on that location's default resource. Requires `Idempotency-
        Key`. Requires `services:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth), and to 20 creations per minute shared by the services, resources, tags and
        caller rules you create.

        Args:
            location_id (None | str | Unset): The location to create the service at, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (ServiceCreate | ServiceCreateDict): A new service with a fixed duration at one location, bookable at
                once. Send at most one of `initial_capacity`, which gives the service a resource of its
                own, or `resource_ids`, which makes it draw on resources of the same location. With
                neither, it draws on the location's default resource (`is_default`); a location with no
                default resource yet is refused with `400 invalid_parameter`. Services booked by the day
                or night, party sizes, buffers and exclusions are set up in Talki.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Service
        """
        return (
            self.with_raw_response.create(
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def delete(
        self,
        service_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a service

         Delete a service for good. Its own resource (`owner_service_id`) is deleted with it, and it stops
        drawing on every other resource. Refused with `service_has_upcoming_bookings` while any of its
        bookings is still to come or under way, even on an inactive service: set `is_active: false` instead,
        which stops new bookings and keeps those. Past and cancelled bookings stay, with `service.id` null
        and the service's name. Sends `service.deleted`, `resource.deleted` for its own resource and
        `resource.updated` for each other resource it drew on. Requires `services:write`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            service_id (str):
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
                service_id=service_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def get(
        self,
        service_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Service:
        """Retrieve a service

         Return one active or inactive service belonging to the account. Requires `services:read`. Limited to
        600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            service_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Service
        """
        return (
            self.with_raw_response.get(
                service_id=service_id,
                talki_version=talki_version,
            )
        ).parse()

    def update(
        self,
        service_id: str,
        *,
        body: ServiceUpdate | ServiceUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Service:
        """Update a service

         Update a service's name, description, price, duration or active state; omitted fields stay
        unchanged. Requires `services:write`. Limited to 120 requests per minute per account (API key) or
        per installation (OAuth).

        Args:
            service_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (ServiceUpdate | ServiceUpdateDict): The service fields you can change. Every field is optional; an
                omitted one is left unchanged. Everything else on a service — booking mode, stay rules,
                quantities, capacity — is read-only here.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Service
        """
        return (
            self.with_raw_response.update(
                service_id=service_id,
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
        is_active: bool | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[Service]:
        """List service changes

         Walk the service-catalogue change feed in commit order. Walking from no cursor until `has_more` is
        false reads every current service. Requires `services:read`. Limited to 600 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of services to return. Default: 50.
            cursor (None | str | Unset): Opaque position in the change feed, from a previous
                response's `next_cursor`. Omit to start from the beginning. Store the last one you
                received: it is how you resume a sync without re-reading the whole catalogue. Not
                interchangeable with another endpoint's cursor.
            is_active (bool | None | Unset): Restrict to services that are switched on (`true`) or off
                (`false`). Omit to get both — which is what an incremental sync needs, since switching a
                service off is a change you must see. Use this only for a point-in-time snapshot.
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
            Page[Service]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """
        return (
            self.with_raw_response.list(
                limit=limit,
                cursor=cursor,
                is_active=is_active,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()


class AsyncServicesResourceWithRawResponse(_resource.Resource):
    """`talki.services.with_raw_response` on `AsyncTalki`: the methods of `talki.services`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def create(
        self,
        *,
        body: ServiceCreate | ServiceCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Service]:
        """`talki.services.create`, returning the whole answer."""
        body = _resource.as_body(body, ServiceCreate)
        return _resource.raw(
            await create_service.asyncio_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def delete(
        self,
        service_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.services.delete`, returning the whole answer."""
        return _resource.raw(
            await delete_service.asyncio_detailed(
                client=self._client,
                service_id=service_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def get(
        self,
        service_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Service]:
        """`talki.services.get`, returning the whole answer."""
        return _resource.raw(
            await get_service.asyncio_detailed(
                client=self._client,
                service_id=service_id,
                talki_version=talki_version,
            )
        )

    async def update(
        self,
        service_id: str,
        *,
        body: ServiceUpdate | ServiceUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Service]:
        """`talki.services.update`, returning the whole answer."""
        body = _resource.as_body(body, ServiceUpdate)
        return _resource.raw(
            await update_service.asyncio_detailed(
                client=self._client,
                service_id=service_id,
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
        is_active: bool | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.AsyncPage[Service]]:
        """`talki.services.list`, returning the whole answer."""

        async def fetch(cursor: None | str | Unset) -> ServiceList:
            return _resource.unwrap(
                await list_services.asyncio_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    is_active=is_active,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            await list_services.asyncio_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                is_active=is_active,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.AsyncPage(page, fetch, cursor))


class AsyncServicesResource(_resource.Resource):
    """`talki.services` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncServicesResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncServicesResourceWithRawResponse(self._client)

    async def create(
        self,
        *,
        body: ServiceCreate | ServiceCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Service:
        """Create a service

         Create a service with a fixed duration, bookable at once, at the location `location_id` names, the
        main location without it. Send at most one of `initial_capacity` or `resource_ids` (resources of the
        same location); with neither, it draws on that location's default resource. Requires `Idempotency-
        Key`. Requires `services:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth), and to 20 creations per minute shared by the services, resources, tags and
        caller rules you create.

        Args:
            location_id (None | str | Unset): The location to create the service at, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (ServiceCreate | ServiceCreateDict): A new service with a fixed duration at one location, bookable at
                once. Send at most one of `initial_capacity`, which gives the service a resource of its
                own, or `resource_ids`, which makes it draw on resources of the same location. With
                neither, it draws on the location's default resource (`is_default`); a location with no
                default resource yet is refused with `400 invalid_parameter`. Services booked by the day
                or night, party sizes, buffers and exclusions are set up in Talki.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Service
        """
        return (
            await self.with_raw_response.create(
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def delete(
        self,
        service_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a service

         Delete a service for good. Its own resource (`owner_service_id`) is deleted with it, and it stops
        drawing on every other resource. Refused with `service_has_upcoming_bookings` while any of its
        bookings is still to come or under way, even on an inactive service: set `is_active: false` instead,
        which stops new bookings and keeps those. Past and cancelled bookings stay, with `service.id` null
        and the service's name. Sends `service.deleted`, `resource.deleted` for its own resource and
        `resource.updated` for each other resource it drew on. Requires `services:write`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            service_id (str):
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
                service_id=service_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def get(
        self,
        service_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Service:
        """Retrieve a service

         Return one active or inactive service belonging to the account. Requires `services:read`. Limited to
        600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            service_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Service
        """
        return (
            await self.with_raw_response.get(
                service_id=service_id,
                talki_version=talki_version,
            )
        ).parse()

    async def update(
        self,
        service_id: str,
        *,
        body: ServiceUpdate | ServiceUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Service:
        """Update a service

         Update a service's name, description, price, duration or active state; omitted fields stay
        unchanged. Requires `services:write`. Limited to 120 requests per minute per account (API key) or
        per installation (OAuth).

        Args:
            service_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (ServiceUpdate | ServiceUpdateDict): The service fields you can change. Every field is optional; an
                omitted one is left unchanged. Everything else on a service — booking mode, stay rules,
                quantities, capacity — is read-only here.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Service
        """
        return (
            await self.with_raw_response.update(
                service_id=service_id,
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
        is_active: bool | None | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPager[Service]:
        """List service changes

         Walk the service-catalogue change feed in commit order. Walking from no cursor until `has_more` is
        false reads every current service. Requires `services:read`. Limited to 600 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of services to return. Default: 50.
            cursor (None | str | Unset): Opaque position in the change feed, from a previous
                response's `next_cursor`. Omit to start from the beginning. Store the last one you
                received: it is how you resume a sync without re-reading the whole catalogue. Not
                interchangeable with another endpoint's cursor.
            is_active (bool | None | Unset): Restrict to services that are switched on (`true`) or off
                (`false`). Omit to get both — which is what an incremental sync needs, since switching a
                service off is a change you must see. Use this only for a point-in-time snapshot.
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
            AsyncPager[Service]: Awaited, this page (an `AsyncPage`). Iterated with `async for`,
            every row from here on, fetching the pages as it goes.
        """

        async def first() -> _pagination.AsyncPage[Service]:
            return (
                await self.with_raw_response.list(
                    limit=limit,
                    cursor=cursor,
                    is_active=is_active,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            ).parse()

        return _pagination.AsyncPager(first)
