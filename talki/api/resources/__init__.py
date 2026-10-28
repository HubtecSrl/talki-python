"""The `resources` operations, one module each, and `ResourcesResource` / `AsyncResourcesResource`,
which `Talki` and `AsyncTalki` expose as `resources`."""

from functools import cached_property

from ... import _resource
from ... import pagination as _pagination
from ...models.resource import Resource
from ...models.resource_create import ResourceCreate, ResourceCreateDict
from ...models.resource_list import ResourceList
from ...models.resource_update import ResourceUpdate, ResourceUpdateDict
from ...types import UNSET, Unset
from . import (
    create_resource,
    delete_resource,
    get_resource,
    list_resources,
    update_resource,
)

__all__ = [
    "AsyncResourcesResource",
    "AsyncResourcesResourceWithRawResponse",
    "ResourcesResource",
    "ResourcesResourceWithRawResponse",
]


class ResourcesResourceWithRawResponse(_resource.Resource):
    """`talki.resources.with_raw_response`: the methods of `talki.resources`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def create(
        self,
        *,
        body: ResourceCreate | ResourceCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Resource]:
        """`talki.resources.create`, returning the whole answer."""
        body = _resource.as_body(body, ResourceCreate)
        return _resource.raw(
            create_resource.sync_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def delete(
        self,
        resource_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.resources.delete`, returning the whole answer."""
        return _resource.raw(
            delete_resource.sync_detailed(
                client=self._client,
                resource_id=resource_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def get(
        self,
        resource_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Resource]:
        """`talki.resources.get`, returning the whole answer."""
        return _resource.raw(
            get_resource.sync_detailed(
                client=self._client,
                resource_id=resource_id,
                talki_version=talki_version,
            )
        )

    def update(
        self,
        resource_id: str,
        *,
        body: ResourceUpdate | ResourceUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Resource]:
        """`talki.resources.update`, returning the whole answer."""
        body = _resource.as_body(body, ResourceUpdate)
        return _resource.raw(
            update_resource.sync_detailed(
                client=self._client,
                resource_id=resource_id,
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
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.Page[Resource]]:
        """`talki.resources.list`, returning the whole answer."""

        def fetch(cursor: None | str | Unset) -> ResourceList:
            return _resource.unwrap(
                list_resources.sync_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            list_resources.sync_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.Page(page, fetch, cursor))


class ResourcesResource(_resource.Resource):
    """`talki.resources`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> ResourcesResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return ResourcesResourceWithRawResponse(self._client)

    def create(
        self,
        *,
        body: ResourceCreate | ResourceCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Resource:
        """Create a resource

         Create a `shared` resource at the location `location_id` names, the main location without it,
        optionally drawn on by existing services of that location. Requires `Idempotency-Key`. Requires
        `resources:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth), and to 20 creations per minute shared by the services, resources, tags and caller rules you
        create.

        Args:
            location_id (None | str | Unset): The location to create the resource at, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (ResourceCreate | ResourceCreateDict): A new `shared` resource at one location: a count of interchangeable
                units, optionally drawn on by existing services of that location. With no `service_ids` it
                limits nothing until a service is linked to it, for example by `POST /v1/services` with
                `resource_ids`. Resources made of sized units are set up in Talki.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Resource
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
        resource_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a resource

         Delete a resource for good, with its unit classes and service links. Refused with
        `resource_is_default` for the default resource (`is_default`), and with
        `resource_required_by_service` when it is the only resource of an active service, or of a service
        booked by the day or night even while inactive: link that service to another resource first.
        Bookings are never cancelled; one that held a unit of this resource keeps its time and loses the
        unit. Sends `resource.deleted` with the resource as it was. Requires `resources:write`. Limited to
        120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            resource_id (str):
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
                resource_id=resource_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def get(
        self,
        resource_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Resource:
        """Retrieve a resource

         Return one resource belonging to the account, with its unit classes and service links. Requires
        `resources:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            resource_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Resource
        """
        return (
            self.with_raw_response.get(
                resource_id=resource_id,
                talki_version=talki_version,
            )
        ).parse()

    def update(
        self,
        resource_id: str,
        *,
        body: ResourceUpdate | ResourceUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Resource:
        """Update a resource

         Rename a resource or set the capacity of a `shared` one. Refused when bookings already exceed it.
        Requires `resources:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            resource_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (ResourceUpdate | ResourceUpdateDict): The two fields you can change on a resource. A capacity below what
                is already booked is refused.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Resource
        """
        return (
            self.with_raw_response.update(
                resource_id=resource_id,
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
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[Resource]:
        """List resource changes

         Walk the capacity change feed in commit order. A resource moves when its unit classes or service
        links change too. Walking from no cursor until `has_more` is false reads every current resource.
        Requires `resources:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of resources to return. Default: 50.
            cursor (None | str | Unset): Opaque position in the change feed, from a previous
                response's `next_cursor`. Omit to start from the beginning. Store the last one you
                received: it is how you resume a sync without re-reading the whole inventory. Not
                interchangeable with another endpoint's cursor.
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
            Page[Resource]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """
        return (
            self.with_raw_response.list(
                limit=limit,
                cursor=cursor,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()


class AsyncResourcesResourceWithRawResponse(_resource.Resource):
    """`talki.resources.with_raw_response` on `AsyncTalki`: the methods of `talki.resources`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def create(
        self,
        *,
        body: ResourceCreate | ResourceCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Resource]:
        """`talki.resources.create`, returning the whole answer."""
        body = _resource.as_body(body, ResourceCreate)
        return _resource.raw(
            await create_resource.asyncio_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def delete(
        self,
        resource_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.resources.delete`, returning the whole answer."""
        return _resource.raw(
            await delete_resource.asyncio_detailed(
                client=self._client,
                resource_id=resource_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def get(
        self,
        resource_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Resource]:
        """`talki.resources.get`, returning the whole answer."""
        return _resource.raw(
            await get_resource.asyncio_detailed(
                client=self._client,
                resource_id=resource_id,
                talki_version=talki_version,
            )
        )

    async def update(
        self,
        resource_id: str,
        *,
        body: ResourceUpdate | ResourceUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Resource]:
        """`talki.resources.update`, returning the whole answer."""
        body = _resource.as_body(body, ResourceUpdate)
        return _resource.raw(
            await update_resource.asyncio_detailed(
                client=self._client,
                resource_id=resource_id,
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
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.AsyncPage[Resource]]:
        """`talki.resources.list`, returning the whole answer."""

        async def fetch(cursor: None | str | Unset) -> ResourceList:
            return _resource.unwrap(
                await list_resources.asyncio_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            await list_resources.asyncio_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.AsyncPage(page, fetch, cursor))


class AsyncResourcesResource(_resource.Resource):
    """`talki.resources` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncResourcesResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncResourcesResourceWithRawResponse(self._client)

    async def create(
        self,
        *,
        body: ResourceCreate | ResourceCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Resource:
        """Create a resource

         Create a `shared` resource at the location `location_id` names, the main location without it,
        optionally drawn on by existing services of that location. Requires `Idempotency-Key`. Requires
        `resources:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth), and to 20 creations per minute shared by the services, resources, tags and caller rules you
        create.

        Args:
            location_id (None | str | Unset): The location to create the resource at, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (ResourceCreate | ResourceCreateDict): A new `shared` resource at one location: a count of interchangeable
                units, optionally drawn on by existing services of that location. With no `service_ids` it
                limits nothing until a service is linked to it, for example by `POST /v1/services` with
                `resource_ids`. Resources made of sized units are set up in Talki.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Resource
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
        resource_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a resource

         Delete a resource for good, with its unit classes and service links. Refused with
        `resource_is_default` for the default resource (`is_default`), and with
        `resource_required_by_service` when it is the only resource of an active service, or of a service
        booked by the day or night even while inactive: link that service to another resource first.
        Bookings are never cancelled; one that held a unit of this resource keeps its time and loses the
        unit. Sends `resource.deleted` with the resource as it was. Requires `resources:write`. Limited to
        120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            resource_id (str):
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
                resource_id=resource_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def get(
        self,
        resource_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Resource:
        """Retrieve a resource

         Return one resource belonging to the account, with its unit classes and service links. Requires
        `resources:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            resource_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Resource
        """
        return (
            await self.with_raw_response.get(
                resource_id=resource_id,
                talki_version=talki_version,
            )
        ).parse()

    async def update(
        self,
        resource_id: str,
        *,
        body: ResourceUpdate | ResourceUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Resource:
        """Update a resource

         Rename a resource or set the capacity of a `shared` one. Refused when bookings already exceed it.
        Requires `resources:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            resource_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (ResourceUpdate | ResourceUpdateDict): The two fields you can change on a resource. A capacity below what
                is already booked is refused.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Resource
        """
        return (
            await self.with_raw_response.update(
                resource_id=resource_id,
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
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPager[Resource]:
        """List resource changes

         Walk the capacity change feed in commit order. A resource moves when its unit classes or service
        links change too. Walking from no cursor until `has_more` is false reads every current resource.
        Requires `resources:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of resources to return. Default: 50.
            cursor (None | str | Unset): Opaque position in the change feed, from a previous
                response's `next_cursor`. Omit to start from the beginning. Store the last one you
                received: it is how you resume a sync without re-reading the whole inventory. Not
                interchangeable with another endpoint's cursor.
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
            AsyncPager[Resource]: Awaited, this page (an `AsyncPage`). Iterated with `async for`,
            every row from here on, fetching the pages as it goes.
        """

        async def first() -> _pagination.AsyncPage[Resource]:
            return (
                await self.with_raw_response.list(
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            ).parse()

        return _pagination.AsyncPager(first)
