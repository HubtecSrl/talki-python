"""The `pending_contacts` operations, one module each, and `PendingContactsResource` / `AsyncPendingContactsResource`,
which `Talki` and `AsyncTalki` expose as `pending_contacts`."""

from ... import _resource
from ...models.contact import Contact
from ...models.pending_contact_approval import PendingContactApproval
from ...models.pending_contact_list import PendingContactList
from ...types import UNSET, Unset
from . import (
    approve_pending_contact,
    discard_pending_contact,
    list_pending_contacts,
)

__all__ = ["AsyncPendingContactsResource", "PendingContactsResource"]


class PendingContactsResource(_resource.Resource):
    """`talki.pending_contacts`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    def approve(
        self,
        pending_id: str,
        *,
        body: PendingContactApproval | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Contact:
        """Approve a pending contact

         Make a pending contact a contact, with any corrections, and return the contact. Requires
        `contacts:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            pending_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (PendingContactApproval | Unset): Corrections to apply while approving; omitted
                fields keep what was heard.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Contact
        """
        return _resource.unwrap(
            approve_pending_contact.sync_detailed(
                client=self._client,
                pending_id=pending_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def discard(
        self,
        pending_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Discard a pending contact

         Forget a pending contact. Requires `contacts:write`. Limited to 120 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            pending_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        _resource.unwrap(
            discard_pending_contact.sync_detailed(
                client=self._client,
                pending_id=pending_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> PendingContactList:
        """List pending contacts

         Return the names the assistant heard that wait for the owner, newest first. Requires
        `contacts:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            PendingContactList
        """
        return _resource.unwrap(
            list_pending_contacts.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class AsyncPendingContactsResource(_resource.Resource):
    """`talki.pending_contacts` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    async def approve(
        self,
        pending_id: str,
        *,
        body: PendingContactApproval | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Contact:
        """Approve a pending contact

         Make a pending contact a contact, with any corrections, and return the contact. Requires
        `contacts:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            pending_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (PendingContactApproval | Unset): Corrections to apply while approving; omitted
                fields keep what was heard.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Contact
        """
        return _resource.unwrap(
            await approve_pending_contact.asyncio_detailed(
                client=self._client,
                pending_id=pending_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def discard(
        self,
        pending_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Discard a pending contact

         Forget a pending contact. Requires `contacts:write`. Limited to 120 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            pending_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        _resource.unwrap(
            await discard_pending_contact.asyncio_detailed(
                client=self._client,
                pending_id=pending_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> PendingContactList:
        """List pending contacts

         Return the names the assistant heard that wait for the owner, newest first. Requires
        `contacts:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            PendingContactList
        """
        return _resource.unwrap(
            await list_pending_contacts.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )
