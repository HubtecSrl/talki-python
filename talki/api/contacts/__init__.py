"""The `contacts` operations, one module each, and `ContactsResource` / `AsyncContactsResource`,
which `Talki` and `AsyncTalki` expose as `contacts`."""

from functools import cached_property

from ... import _resource
from ... import pagination as _pagination
from ...models.contact import Contact
from ...models.contact_list import ContactList
from ...models.contact_upsert import ContactUpsert, ContactUpsertDict
from ...types import UNSET, Unset
from . import (
    delete_contact,
    get_contact,
    list_contacts,
    upsert_contact,
)

__all__ = [
    "AsyncContactsResource",
    "AsyncContactsResourceWithRawResponse",
    "ContactsResource",
    "ContactsResourceWithRawResponse",
]


class ContactsResourceWithRawResponse(_resource.Resource):
    """`talki.contacts.with_raw_response`: the methods of `talki.contacts`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def delete(
        self,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.contacts.delete`, returning the whole answer."""
        return _resource.raw(
            delete_contact.sync_detailed(
                client=self._client,
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def get(
        self,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Contact]:
        """`talki.contacts.get`, returning the whole answer."""
        return _resource.raw(
            get_contact.sync_detailed(
                client=self._client,
                contact_id=contact_id,
                talki_version=talki_version,
            )
        )

    def upsert(
        self,
        *,
        body: ContactUpsert | ContactUpsertDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Contact]:
        """`talki.contacts.upsert`, returning the whole answer."""
        body = _resource.as_body(body, ContactUpsert)
        return _resource.raw(
            upsert_contact.sync_detailed(
                client=self._client,
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
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.Page[Contact]]:
        """`talki.contacts.list`, returning the whole answer."""

        def fetch(cursor: None | str | Unset) -> ContactList:
            return _resource.unwrap(
                list_contacts.sync_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            list_contacts.sync_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.Page(page, fetch, cursor))


class ContactsResource(_resource.Resource):
    """`talki.contacts`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> ContactsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return ContactsResourceWithRawResponse(self._client)

    def delete(
        self,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a contact

         Delete a contact with its tags and `external_id`. Calls and appointments are kept. If the number is
        in an address book the owner connected, its next call creates the contact again under a new `id`.
        Requires `contacts:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            contact_id (str):
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
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def get(
        self,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Contact:
        """Retrieve a contact

         Return one curated contact belonging to the account. Requires `contacts:read`. Limited to 600
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            contact_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Contact
        """
        return (
            self.with_raw_response.get(
                contact_id=contact_id,
                talki_version=talki_version,
            )
        ).parse()

    def upsert(
        self,
        *,
        body: ContactUpsert | ContactUpsertDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Contact:
        """Upsert a contact

         Create or update a trusted contact by phone number or external reference. Requires `contacts:write`.
        Limited to 120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (ContactUpsert | ContactUpsertDict): Create or update the contact with this phone number: the number is
                the identity, and `external_id` is your cross-reference for finding it again after a
                number changes. A name written here is not overwritten by what the assistant hears on
                later calls. On a contact whose name was only guessed from a call, sending either name
                replaces both: the one you omit is cleared.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Contact
        """
        return (
            self.with_raw_response.upsert(
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
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[Contact]:
        """List contact changes

         Walk the curated-contact change feed in commit order. Requires `contacts:read`. Limited to 600
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of contacts to return. Default: 50.
            cursor (None | str | Unset): Opaque position in the change feed, from a previous
                response's `next_cursor`. Omit to start from the beginning. Store the last one you
                received: it is how you resume a sync without re-reading the whole address book. Not
                interchangeable with another endpoint's cursor.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Page[Contact]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """
        return (
            self.with_raw_response.list(
                limit=limit,
                cursor=cursor,
                talki_version=talki_version,
            )
        ).parse()


class AsyncContactsResourceWithRawResponse(_resource.Resource):
    """`talki.contacts.with_raw_response` on `AsyncTalki`: the methods of `talki.contacts`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def delete(
        self,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.contacts.delete`, returning the whole answer."""
        return _resource.raw(
            await delete_contact.asyncio_detailed(
                client=self._client,
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def get(
        self,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Contact]:
        """`talki.contacts.get`, returning the whole answer."""
        return _resource.raw(
            await get_contact.asyncio_detailed(
                client=self._client,
                contact_id=contact_id,
                talki_version=talki_version,
            )
        )

    async def upsert(
        self,
        *,
        body: ContactUpsert | ContactUpsertDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Contact]:
        """`talki.contacts.upsert`, returning the whole answer."""
        body = _resource.as_body(body, ContactUpsert)
        return _resource.raw(
            await upsert_contact.asyncio_detailed(
                client=self._client,
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
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.AsyncPage[Contact]]:
        """`talki.contacts.list`, returning the whole answer."""

        async def fetch(cursor: None | str | Unset) -> ContactList:
            return _resource.unwrap(
                await list_contacts.asyncio_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            await list_contacts.asyncio_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.AsyncPage(page, fetch, cursor))


class AsyncContactsResource(_resource.Resource):
    """`talki.contacts` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncContactsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncContactsResourceWithRawResponse(self._client)

    async def delete(
        self,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a contact

         Delete a contact with its tags and `external_id`. Calls and appointments are kept. If the number is
        in an address book the owner connected, its next call creates the contact again under a new `id`.
        Requires `contacts:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            contact_id (str):
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
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def get(
        self,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Contact:
        """Retrieve a contact

         Return one curated contact belonging to the account. Requires `contacts:read`. Limited to 600
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            contact_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Contact
        """
        return (
            await self.with_raw_response.get(
                contact_id=contact_id,
                talki_version=talki_version,
            )
        ).parse()

    async def upsert(
        self,
        *,
        body: ContactUpsert | ContactUpsertDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Contact:
        """Upsert a contact

         Create or update a trusted contact by phone number or external reference. Requires `contacts:write`.
        Limited to 120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (ContactUpsert | ContactUpsertDict): Create or update the contact with this phone number: the number is
                the identity, and `external_id` is your cross-reference for finding it again after a
                number changes. A name written here is not overwritten by what the assistant hears on
                later calls. On a contact whose name was only guessed from a call, sending either name
                replaces both: the one you omit is cleared.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Contact
        """
        return (
            await self.with_raw_response.upsert(
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
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPager[Contact]:
        """List contact changes

         Walk the curated-contact change feed in commit order. Requires `contacts:read`. Limited to 600
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of contacts to return. Default: 50.
            cursor (None | str | Unset): Opaque position in the change feed, from a previous
                response's `next_cursor`. Omit to start from the beginning. Store the last one you
                received: it is how you resume a sync without re-reading the whole address book. Not
                interchangeable with another endpoint's cursor.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AsyncPager[Contact]: Awaited, this page (an `AsyncPage`). Iterated with `async for`,
            every row from here on, fetching the pages as it goes.
        """

        async def first() -> _pagination.AsyncPage[Contact]:
            return (
                await self.with_raw_response.list(
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            ).parse()

        return _pagination.AsyncPager(first)
