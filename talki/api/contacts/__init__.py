"""The `contacts` operations, one module each, and `ContactsResource` / `AsyncContactsResource`,
which `Talki` and `AsyncTalki` expose as `contacts`."""

from ... import _resource
from ... import pagination as _pagination
from ...models.contact import Contact
from ...models.contact_list import ContactList
from ...models.contact_upsert import ContactUpsert
from ...types import UNSET, Unset
from . import (
    delete_contact,
    get_contact,
    list_contacts,
    upsert_contact,
)

__all__ = ["AsyncContactsResource", "ContactsResource"]


class ContactsResource(_resource.Resource):
    """`talki.contacts`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

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
        _resource.unwrap(
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
        return _resource.unwrap(
            get_contact.sync_detailed(
                client=self._client,
                contact_id=contact_id,
                talki_version=talki_version,
            )
        )

    def upsert(
        self,
        *,
        body: ContactUpsert,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Contact:
        """Upsert a contact

         Create or update a trusted contact by phone number or external reference. Requires `contacts:write`.
        Limited to 120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (ContactUpsert): Create or update the contact with this phone number: the number is
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
        return _resource.unwrap(
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

        def fetch(cursor: None | str | Unset) -> ContactList:
            return _resource.unwrap(
                list_contacts.sync_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            )

        return _pagination.Page.first(fetch, cursor)


class AsyncContactsResource(_resource.Resource):
    """`talki.contacts` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

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
        _resource.unwrap(
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
        return _resource.unwrap(
            await get_contact.asyncio_detailed(
                client=self._client,
                contact_id=contact_id,
                talki_version=talki_version,
            )
        )

    async def upsert(
        self,
        *,
        body: ContactUpsert,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Contact:
        """Upsert a contact

         Create or update a trusted contact by phone number or external reference. Requires `contacts:write`.
        Limited to 120 requests per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (ContactUpsert): Create or update the contact with this phone number: the number is
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
        return _resource.unwrap(
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
    ) -> _pagination.AsyncPage[Contact]:
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
            AsyncPage[Contact]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """

        async def fetch(cursor: None | str | Unset) -> ContactList:
            return _resource.unwrap(
                await list_contacts.asyncio_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            )

        return await _pagination.AsyncPage.first(fetch, cursor)
