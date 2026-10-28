"""The `pending_contacts` operations, one module each, and `PendingContactsResource` / `AsyncPendingContactsResource`,
which `Talki` and `AsyncTalki` expose as `pending_contacts`."""

from functools import cached_property

from ... import _resource
from ...models.contact import Contact
from ...models.pending_contact_approval import PendingContactApproval, PendingContactApprovalDict
from ...models.pending_contact_list import PendingContactList
from ...types import UNSET, Unset
from . import (
    approve_pending_contact,
    discard_pending_contact,
    list_pending_contacts,
)

__all__ = [
    "AsyncPendingContactsResource",
    "AsyncPendingContactsResourceWithRawResponse",
    "PendingContactsResource",
    "PendingContactsResourceWithRawResponse",
]


class PendingContactsResourceWithRawResponse(_resource.Resource):
    """`talki.pending_contacts.with_raw_response`: the methods of `talki.pending_contacts`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def approve(
        self,
        pending_id: str,
        *,
        body: PendingContactApproval | PendingContactApprovalDict | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Contact]:
        """`talki.pending_contacts.approve`, returning the whole answer."""
        if not isinstance(body, Unset):
            body = _resource.as_body(body, PendingContactApproval)
        return _resource.raw(
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
    ) -> _resource.RawResponse[None]:
        """`talki.pending_contacts.discard`, returning the whole answer."""
        return _resource.raw(
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
    ) -> _resource.RawResponse[PendingContactList]:
        """`talki.pending_contacts.list`, returning the whole answer."""
        return _resource.raw(
            list_pending_contacts.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class PendingContactsResource(_resource.Resource):
    """`talki.pending_contacts`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> PendingContactsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return PendingContactsResourceWithRawResponse(self._client)

    def approve(
        self,
        pending_id: str,
        *,
        body: PendingContactApproval | PendingContactApprovalDict | Unset = UNSET,
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
        return (
            self.with_raw_response.approve(
                pending_id=pending_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

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
        (
            self.with_raw_response.discard(
                pending_id=pending_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

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
        return (
            self.with_raw_response.list(
                talki_version=talki_version,
            )
        ).parse()


class AsyncPendingContactsResourceWithRawResponse(_resource.Resource):
    """`talki.pending_contacts.with_raw_response` on `AsyncTalki`: the methods of `talki.pending_contacts`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def approve(
        self,
        pending_id: str,
        *,
        body: PendingContactApproval | PendingContactApprovalDict | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Contact]:
        """`talki.pending_contacts.approve`, returning the whole answer."""
        if not isinstance(body, Unset):
            body = _resource.as_body(body, PendingContactApproval)
        return _resource.raw(
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
    ) -> _resource.RawResponse[None]:
        """`talki.pending_contacts.discard`, returning the whole answer."""
        return _resource.raw(
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
    ) -> _resource.RawResponse[PendingContactList]:
        """`talki.pending_contacts.list`, returning the whole answer."""
        return _resource.raw(
            await list_pending_contacts.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class AsyncPendingContactsResource(_resource.Resource):
    """`talki.pending_contacts` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncPendingContactsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncPendingContactsResourceWithRawResponse(self._client)

    async def approve(
        self,
        pending_id: str,
        *,
        body: PendingContactApproval | PendingContactApprovalDict | Unset = UNSET,
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
        return (
            await self.with_raw_response.approve(
                pending_id=pending_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

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
        (
            await self.with_raw_response.discard(
                pending_id=pending_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

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
        return (
            await self.with_raw_response.list(
                talki_version=talki_version,
            )
        ).parse()
