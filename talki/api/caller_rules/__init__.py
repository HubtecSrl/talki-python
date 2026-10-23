"""The `caller_rules` operations, one module each, and `CallerRulesResource` / `AsyncCallerRulesResource`,
which `Talki` and `AsyncTalki` expose as `caller_rules`."""

from ... import _resource
from ... import pagination as _pagination
from ...models.blocked_call_attempt import BlockedCallAttempt
from ...models.blocked_call_attempt_list import BlockedCallAttemptList
from ...models.caller_rule import CallerRule
from ...models.caller_rule_create import CallerRuleCreate
from ...models.caller_rule_kind import CallerRuleKind
from ...models.caller_rule_list import CallerRuleList
from ...models.caller_rule_update import CallerRuleUpdate
from ...types import UNSET, Unset
from . import (
    create_caller_rule,
    delete_caller_rule,
    list_blocked_call_attempts,
    list_caller_rules,
    update_caller_rule,
)

__all__ = ["AsyncCallerRulesResource", "CallerRulesResource"]


class CallerRulesResource(_resource.Resource):
    """`talki.caller_rules`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    def create(
        self,
        *,
        body: CallerRuleCreate,
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
            body (CallerRuleCreate): A number to add. `201` creates a rule; `200` means the number
                already had one, which was moved or relabelled as the request asks, or returned unchanged.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallerRule
        """
        return _resource.unwrap(
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
        _resource.unwrap(
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

        return _pagination.Page.first(fetch, cursor)

    def update(
        self,
        rule_id: str,
        *,
        body: CallerRuleUpdate,
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
            body (CallerRuleUpdate): A partial edit of a caller rule.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallerRule
        """
        return _resource.unwrap(
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

        return _pagination.Page.first(fetch, cursor)


class AsyncCallerRulesResource(_resource.Resource):
    """`talki.caller_rules` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    async def create(
        self,
        *,
        body: CallerRuleCreate,
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
            body (CallerRuleCreate): A number to add. `201` creates a rule; `200` means the number
                already had one, which was moved or relabelled as the request asks, or returned unchanged.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallerRule
        """
        return _resource.unwrap(
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
        _resource.unwrap(
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
    ) -> _pagination.AsyncPage[BlockedCallAttempt]:
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
            AsyncPage[BlockedCallAttempt]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """

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

        return await _pagination.AsyncPage.first(fetch, cursor)

    async def update(
        self,
        rule_id: str,
        *,
        body: CallerRuleUpdate,
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
            body (CallerRuleUpdate): A partial edit of a caller rule.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            CallerRule
        """
        return _resource.unwrap(
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
    ) -> _pagination.AsyncPage[CallerRule]:
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
            AsyncPage[CallerRule]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """

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

        return await _pagination.AsyncPage.first(fetch, cursor)
