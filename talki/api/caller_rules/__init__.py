"""The `caller_rules` operations, one module each, and `CallerRulesResource` / `AsyncCallerRulesResource`,
which `Talki` and `AsyncTalki` expose as `caller_rules`."""

from functools import cached_property

from ... import _resource
from ... import pagination as _pagination
from ...models.blocked_call_attempt import BlockedCallAttempt
from ...models.blocked_call_attempt_list import BlockedCallAttemptList
from ...models.caller_rule import CallerRule
from ...models.caller_rule_create import CallerRuleCreate, CallerRuleCreateDict
from ...models.caller_rule_kind import CallerRuleKind
from ...models.caller_rule_list import CallerRuleList
from ...models.caller_rule_update import CallerRuleUpdate, CallerRuleUpdateDict
from ...types import UNSET, Unset
from . import (
    create_caller_rule,
    delete_caller_rule,
    list_blocked_call_attempts,
    list_caller_rules,
    update_caller_rule,
)

__all__ = [
    "AsyncCallerRulesResource",
    "AsyncCallerRulesResourceWithRawResponse",
    "CallerRulesResource",
    "CallerRulesResourceWithRawResponse",
]


class CallerRulesResourceWithRawResponse(_resource.Resource):
    """`talki.caller_rules.with_raw_response`: the methods of `talki.caller_rules`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def create(
        self,
        *,
        body: CallerRuleCreate | CallerRuleCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[CallerRule]:
        """`talki.caller_rules.create`, returning the whole answer."""
        body = _resource.as_body(body, CallerRuleCreate)
        return _resource.raw(
            create_caller_rule.sync_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def delete(
        self,
        rule_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.caller_rules.delete`, returning the whole answer."""
        return _resource.raw(
            delete_caller_rule.sync_detailed(
                client=self._client,
                rule_id=rule_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def list_blocked_call_attempts(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.Page[BlockedCallAttempt]]:
        """`talki.caller_rules.list_blocked_call_attempts`, returning the whole answer."""

        def fetch(cursor: None | str | Unset) -> BlockedCallAttemptList:
            return _resource.unwrap(
                list_blocked_call_attempts.sync_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            list_blocked_call_attempts.sync_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.Page(page, fetch, cursor))

    def update(
        self,
        rule_id: str,
        *,
        body: CallerRuleUpdate | CallerRuleUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[CallerRule]:
        """`talki.caller_rules.update`, returning the whole answer."""
        body = _resource.as_body(body, CallerRuleUpdate)
        return _resource.raw(
            update_caller_rule.sync_detailed(
                client=self._client,
                rule_id=rule_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def list(
        self,
        *,
        kind: CallerRuleKind | None | Unset = UNSET,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.Page[CallerRule]]:
        """`talki.caller_rules.list`, returning the whole answer."""

        def fetch(cursor: None | str | Unset) -> CallerRuleList:
            return _resource.unwrap(
                list_caller_rules.sync_detailed(
                    client=self._client,
                    kind=kind,
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            list_caller_rules.sync_detailed(
                client=self._client,
                kind=kind,
                limit=limit,
                cursor=cursor,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.Page(page, fetch, cursor))


class CallerRulesResource(_resource.Resource):
    """`talki.caller_rules`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> CallerRulesResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return CallerRulesResourceWithRawResponse(self._client)

    def create(
        self,
        *,
        body: CallerRuleCreate | CallerRuleCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> CallerRule:
        """Add a caller rule

         Add a number to the VIP or blocked list: `201` with the new rule. A number that already has a rule
        answers `200` with it, moved or relabelled as the request asks, or unchanged. Requires `Idempotency-
        Key`. Requires `contacts:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth), and to 20 creations per minute shared by the services, resources, tags and
        caller rules you create.

        Args:
            location_id (None | str | Unset): The location to add the number at, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (CallerRuleCreate | CallerRuleCreateDict): A number to add. `201` creates a rule; `200` means the number
                already had one, which was moved or relabelled as the request asks, or returned unchanged.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallerRule
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
        rule_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a caller rule

         Remove a number from its list. Requires `contacts:write`. Limited to 120 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            rule_id (str):
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
                rule_id=rule_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list_blocked_call_attempts(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[BlockedCallAttempt]:
        """List blocked calls

         Return the calls refused because their number is blocked, newest first. Requires `contacts:read`.
        Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of attempts to return. Default: 50.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page.
            location_id (None | str | Unset): Only the records of this location, an id from `GET
                /v1/locations` (inactive ones included). Omit for every location: each record carries its
                `location_id`.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Page[BlockedCallAttempt]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """
        return (
            self.with_raw_response.list_blocked_call_attempts(
                limit=limit,
                cursor=cursor,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()

    def update(
        self,
        rule_id: str,
        *,
        body: CallerRuleUpdate | CallerRuleUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> CallerRule:
        """Update a caller rule

         Move a rule to the other list or relabel it. Requires `contacts:write`. Limited to 120 requests per
        minute per account (API key) or per installation (OAuth).

        Args:
            rule_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (CallerRuleUpdate | CallerRuleUpdateDict): A partial edit of a caller rule.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallerRule
        """
        return (
            self.with_raw_response.update(
                rule_id=rule_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list(
        self,
        *,
        kind: CallerRuleKind | None | Unset = UNSET,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[CallerRule]:
        """List caller rules

         Return the VIP and blocked numbers, newest first. Requires `contacts:read`. Limited to 600 requests
        per minute per account (API key) or per installation (OAuth).

        Args:
            kind (CallerRuleKind | None | Unset): Only `vip` or only `blocked` numbers. Omit for both.
            limit (int | Unset): Maximum number of rules to return. Default: 50.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page.
            location_id (None | str | Unset): Only the records of this location, an id from `GET
                /v1/locations` (inactive ones included). Omit for every location: each record carries its
                `location_id`.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Page[CallerRule]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """
        return (
            self.with_raw_response.list(
                kind=kind,
                limit=limit,
                cursor=cursor,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()


class AsyncCallerRulesResourceWithRawResponse(_resource.Resource):
    """`talki.caller_rules.with_raw_response` on `AsyncTalki`: the methods of `talki.caller_rules`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def create(
        self,
        *,
        body: CallerRuleCreate | CallerRuleCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[CallerRule]:
        """`talki.caller_rules.create`, returning the whole answer."""
        body = _resource.as_body(body, CallerRuleCreate)
        return _resource.raw(
            await create_caller_rule.asyncio_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def delete(
        self,
        rule_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.caller_rules.delete`, returning the whole answer."""
        return _resource.raw(
            await delete_caller_rule.asyncio_detailed(
                client=self._client,
                rule_id=rule_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def list_blocked_call_attempts(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.AsyncPage[BlockedCallAttempt]]:
        """`talki.caller_rules.list_blocked_call_attempts`, returning the whole answer."""

        async def fetch(cursor: None | str | Unset) -> BlockedCallAttemptList:
            return _resource.unwrap(
                await list_blocked_call_attempts.asyncio_detailed(
                    client=self._client,
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            await list_blocked_call_attempts.asyncio_detailed(
                client=self._client,
                limit=limit,
                cursor=cursor,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.AsyncPage(page, fetch, cursor))

    async def update(
        self,
        rule_id: str,
        *,
        body: CallerRuleUpdate | CallerRuleUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[CallerRule]:
        """`talki.caller_rules.update`, returning the whole answer."""
        body = _resource.as_body(body, CallerRuleUpdate)
        return _resource.raw(
            await update_caller_rule.asyncio_detailed(
                client=self._client,
                rule_id=rule_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def list(
        self,
        *,
        kind: CallerRuleKind | None | Unset = UNSET,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.AsyncPage[CallerRule]]:
        """`talki.caller_rules.list`, returning the whole answer."""

        async def fetch(cursor: None | str | Unset) -> CallerRuleList:
            return _resource.unwrap(
                await list_caller_rules.asyncio_detailed(
                    client=self._client,
                    kind=kind,
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            await list_caller_rules.asyncio_detailed(
                client=self._client,
                kind=kind,
                limit=limit,
                cursor=cursor,
                location_id=location_id,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.AsyncPage(page, fetch, cursor))


class AsyncCallerRulesResource(_resource.Resource):
    """`talki.caller_rules` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncCallerRulesResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncCallerRulesResourceWithRawResponse(self._client)

    async def create(
        self,
        *,
        body: CallerRuleCreate | CallerRuleCreateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> CallerRule:
        """Add a caller rule

         Add a number to the VIP or blocked list: `201` with the new rule. A number that already has a rule
        answers `200` with it, moved or relabelled as the request asks, or unchanged. Requires `Idempotency-
        Key`. Requires `contacts:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth), and to 20 creations per minute shared by the services, resources, tags and
        caller rules you create.

        Args:
            location_id (None | str | Unset): The location to add the number at, an id from `GET
                /v1/locations` (inactive ones included). Omit it for the main location.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (CallerRuleCreate | CallerRuleCreateDict): A number to add. `201` creates a rule; `200` means the number
                already had one, which was moved or relabelled as the request asks, or returned unchanged.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallerRule
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
        rule_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a caller rule

         Remove a number from its list. Requires `contacts:write`. Limited to 120 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            rule_id (str):
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
                rule_id=rule_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list_blocked_call_attempts(
        self,
        *,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPager[BlockedCallAttempt]:
        """List blocked calls

         Return the calls refused because their number is blocked, newest first. Requires `contacts:read`.
        Limited to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            limit (int | Unset): Maximum number of attempts to return. Default: 50.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page.
            location_id (None | str | Unset): Only the records of this location, an id from `GET
                /v1/locations` (inactive ones included). Omit for every location: each record carries its
                `location_id`.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AsyncPager[BlockedCallAttempt]: Awaited, this page (an `AsyncPage`). Iterated with `async for`,
            every row from here on, fetching the pages as it goes.
        """

        async def first() -> _pagination.AsyncPage[BlockedCallAttempt]:
            return (
                await self.with_raw_response.list_blocked_call_attempts(
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            ).parse()

        return _pagination.AsyncPager(first)

    async def update(
        self,
        rule_id: str,
        *,
        body: CallerRuleUpdate | CallerRuleUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> CallerRule:
        """Update a caller rule

         Move a rule to the other list or relabel it. Requires `contacts:write`. Limited to 120 requests per
        minute per account (API key) or per installation (OAuth).

        Args:
            rule_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (CallerRuleUpdate | CallerRuleUpdateDict): A partial edit of a caller rule.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallerRule
        """
        return (
            await self.with_raw_response.update(
                rule_id=rule_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list(
        self,
        *,
        kind: CallerRuleKind | None | Unset = UNSET,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPager[CallerRule]:
        """List caller rules

         Return the VIP and blocked numbers, newest first. Requires `contacts:read`. Limited to 600 requests
        per minute per account (API key) or per installation (OAuth).

        Args:
            kind (CallerRuleKind | None | Unset): Only `vip` or only `blocked` numbers. Omit for both.
            limit (int | Unset): Maximum number of rules to return. Default: 50.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page.
            location_id (None | str | Unset): Only the records of this location, an id from `GET
                /v1/locations` (inactive ones included). Omit for every location: each record carries its
                `location_id`.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AsyncPager[CallerRule]: Awaited, this page (an `AsyncPage`). Iterated with `async for`,
            every row from here on, fetching the pages as it goes.
        """

        async def first() -> _pagination.AsyncPage[CallerRule]:
            return (
                await self.with_raw_response.list(
                    kind=kind,
                    limit=limit,
                    cursor=cursor,
                    location_id=location_id,
                    talki_version=talki_version,
                )
            ).parse()

        return _pagination.AsyncPager(first)
