"""The `account` operations, one module each, and `AccountResource` / `AsyncAccountResource`,
which `Talki` and `AsyncTalki` expose as `account`."""

from functools import cached_property

from ... import _resource
from ...models.account import Account
from ...models.account_update import AccountUpdate, AccountUpdateDict
from ...models.forwarding_check import ForwardingCheck
from ...types import UNSET, Unset
from . import (
    complete_onboarding,
    get_account,
    get_forwarding_check,
    start_forwarding_check,
    update_account,
)

__all__ = [
    "AsyncAccountResource",
    "AsyncAccountResourceWithRawResponse",
    "AccountResource",
    "AccountResourceWithRawResponse",
]


class AccountResourceWithRawResponse(_resource.Resource):
    """`talki.account.with_raw_response`: the methods of `talki.account`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def complete_onboarding(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Account]:
        """`talki.account.complete_onboarding`, returning the whole answer."""
        return _resource.raw(
            complete_onboarding.sync_detailed(
                client=self._client,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Account]:
        """`talki.account.get`, returning the whole answer."""
        return _resource.raw(
            get_account.sync_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    def get_forwarding_check(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[ForwardingCheck]:
        """`talki.account.get_forwarding_check`, returning the whole answer."""
        return _resource.raw(
            get_forwarding_check.sync_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    def start_forwarding_check(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[ForwardingCheck]:
        """`talki.account.start_forwarding_check`, returning the whole answer."""
        return _resource.raw(
            start_forwarding_check.sync_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def update(
        self,
        *,
        body: AccountUpdate | AccountUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
        if_match: str | Unset = UNSET,
    ) -> _resource.RawResponse[Account]:
        """`talki.account.update`, returning the whole answer."""
        body = _resource.as_body(body, AccountUpdate)
        return _resource.raw(
            update_account.sync_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
                if_match=if_match,
            )
        )


class AccountResource(_resource.Resource):
    """`talki.account`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AccountResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AccountResourceWithRawResponse(self._client)

    def complete_onboarding(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Account:
        """Complete onboarding

         Mark the account's setup as finished, so the Talki app does not open its setup wizard. Idempotent;
        it is never undone. Requires `account:write`. Limited to 120 requests per minute per account (API
        key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Account
        """
        return (
            self.with_raw_response.complete_onboarding(
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> Account:
        """Retrieve the authenticated account

         Validate the API key and return the Talki account it belongs to, with everything `PATCH /v1/account`
        can change, the Talki number and the onboarding state. Requires `account:read`. Limited to 60
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): The location whose settings to read, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Account
        """
        return (
            self.with_raw_response.get(
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()

    def get_forwarding_check(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> ForwardingCheck:
        """Retrieve the forwarding check

         Return the state of the latest forwarding check of one location's line, the main location's unless
        `location_id` names another, and when forwarding was last proven. Requires `account:read`. Limited
        to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): The location whose latest check to read, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            ForwardingCheck
        """
        return (
            self.with_raw_response.get_forwarding_check(
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()

    def start_forwarding_check(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> ForwardingCheck:
        """Start a forwarding check

         Ring one location's `forwarding_number` from its `phone_number`, the main location's unless
        `location_id` names another, then poll `GET /v1/forwarding_check` with the same `location_id`. One
        check at a time per location; at most 3 an hour per location, and 30 an hour per OAuth app across
        all the accounts it is installed on and their locations, past which the answer is `429
        check_quota_exceeded` with `Retry-After`. Refused in test mode, and for an inactive location
        (`phone_number_missing`). Requires `account:write`. Limited to 120 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): The location whose line to ring, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            ForwardingCheck
        """
        return (
            self.with_raw_response.start_forwarding_check(
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def update(
        self,
        *,
        body: AccountUpdate | AccountUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
        if_match: str | Unset = UNSET,
    ) -> Account:
        """Update the assistant settings

         Change any of the account's writable fields: the assistant's settings, the transfer numbers or the
        forwarding number. Omitted fields stay unchanged; a body with none of them is refused. A custom
        `call_opening` needs a plan that includes it, and `store_transcripts: false` is refused with a test-
        mode credential. Send `If-Match` with the `ETag` of your last read to be refused rather than
        overwrite a change made since. Requires `account:write`. Limited to 120 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): The location whose settings to change, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            if_match (str | Unset):
            body (AccountUpdate | AccountUpdateDict): The settings you can change. Every field is optional and an omitted
                one is left unchanged, but send at least one. A `null` or empty text clears it; a voice, a
                switch or the transfer list cannot be null. With `?location_id=`, a location's own
                settings change at that location only, and the account's switches at every location.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Account
        """
        return (
            self.with_raw_response.update(
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
                if_match=if_match,
            )
        ).parse()


class AsyncAccountResourceWithRawResponse(_resource.Resource):
    """`talki.account.with_raw_response` on `AsyncTalki`: the methods of `talki.account`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def complete_onboarding(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Account]:
        """`talki.account.complete_onboarding`, returning the whole answer."""
        return _resource.raw(
            await complete_onboarding.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Account]:
        """`talki.account.get`, returning the whole answer."""
        return _resource.raw(
            await get_account.asyncio_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    async def get_forwarding_check(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[ForwardingCheck]:
        """`talki.account.get_forwarding_check`, returning the whole answer."""
        return _resource.raw(
            await get_forwarding_check.asyncio_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    async def start_forwarding_check(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[ForwardingCheck]:
        """`talki.account.start_forwarding_check`, returning the whole answer."""
        return _resource.raw(
            await start_forwarding_check.asyncio_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def update(
        self,
        *,
        body: AccountUpdate | AccountUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
        if_match: str | Unset = UNSET,
    ) -> _resource.RawResponse[Account]:
        """`talki.account.update`, returning the whole answer."""
        body = _resource.as_body(body, AccountUpdate)
        return _resource.raw(
            await update_account.asyncio_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
                if_match=if_match,
            )
        )


class AsyncAccountResource(_resource.Resource):
    """`talki.account` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncAccountResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncAccountResourceWithRawResponse(self._client)

    async def complete_onboarding(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Account:
        """Complete onboarding

         Mark the account's setup as finished, so the Talki app does not open its setup wizard. Idempotent;
        it is never undone. Requires `account:write`. Limited to 120 requests per minute per account (API
        key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Account
        """
        return (
            await self.with_raw_response.complete_onboarding(
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> Account:
        """Retrieve the authenticated account

         Validate the API key and return the Talki account it belongs to, with everything `PATCH /v1/account`
        can change, the Talki number and the onboarding state. Requires `account:read`. Limited to 60
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): The location whose settings to read, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Account
        """
        return (
            await self.with_raw_response.get(
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()

    async def get_forwarding_check(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> ForwardingCheck:
        """Retrieve the forwarding check

         Return the state of the latest forwarding check of one location's line, the main location's unless
        `location_id` names another, and when forwarding was last proven. Requires `account:read`. Limited
        to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): The location whose latest check to read, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            ForwardingCheck
        """
        return (
            await self.with_raw_response.get_forwarding_check(
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()

    async def start_forwarding_check(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> ForwardingCheck:
        """Start a forwarding check

         Ring one location's `forwarding_number` from its `phone_number`, the main location's unless
        `location_id` names another, then poll `GET /v1/forwarding_check` with the same `location_id`. One
        check at a time per location; at most 3 an hour per location, and 30 an hour per OAuth app across
        all the accounts it is installed on and their locations, past which the answer is `429
        check_quota_exceeded` with `Retry-After`. Refused in test mode, and for an inactive location
        (`phone_number_missing`). Requires `account:write`. Limited to 120 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): The location whose line to ring, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            ForwardingCheck
        """
        return (
            await self.with_raw_response.start_forwarding_check(
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def update(
        self,
        *,
        body: AccountUpdate | AccountUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
        if_match: str | Unset = UNSET,
    ) -> Account:
        """Update the assistant settings

         Change any of the account's writable fields: the assistant's settings, the transfer numbers or the
        forwarding number. Omitted fields stay unchanged; a body with none of them is refused. A custom
        `call_opening` needs a plan that includes it, and `store_transcripts: false` is refused with a test-
        mode credential. Send `If-Match` with the `ETag` of your last read to be refused rather than
        overwrite a change made since. Requires `account:write`. Limited to 120 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): The location whose settings to change, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            if_match (str | Unset):
            body (AccountUpdate | AccountUpdateDict): The settings you can change. Every field is optional and an omitted
                one is left unchanged, but send at least one. A `null` or empty text clears it; a voice, a
                switch or the transfer list cannot be null. With `?location_id=`, a location's own
                settings change at that location only, and the account's switches at every location.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Account
        """
        return (
            await self.with_raw_response.update(
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
                if_match=if_match,
            )
        ).parse()
