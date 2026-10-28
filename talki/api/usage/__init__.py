"""The `usage` operations, one module each, and `UsageResource` / `AsyncUsageResource`,
which `Talki` and `AsyncTalki` expose as `usage`."""

from functools import cached_property

from ... import _resource
from ...models.usage import Usage
from ...models.usage_history import UsageHistory
from ...types import UNSET, Unset
from . import (
    get_usage,
    get_usage_history,
)

__all__ = [
    "AsyncUsageResource",
    "AsyncUsageResourceWithRawResponse",
    "UsageResource",
    "UsageResourceWithRawResponse",
]


class UsageResourceWithRawResponse(_resource.Resource):
    """`talki.usage.with_raw_response`: the methods of `talki.usage`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def get(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Usage]:
        """`talki.usage.get`, returning the whole answer."""
        return _resource.raw(
            get_usage.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )

    def get_history(
        self,
        *,
        from_: None | str | Unset = UNSET,
        to: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[UsageHistory]:
        """`talki.usage.get_history`, returning the whole answer."""
        return _resource.raw(
            get_usage_history.sync_detailed(
                client=self._client,
                from_=from_,
                to=to,
                talki_version=talki_version,
            )
        )


class UsageResource(_resource.Resource):
    """`talki.usage`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> UsageResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return UsageResourceWithRawResponse(self._client)

    def get(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Usage:
        """Retrieve usage

         Return the talk time used in the current period, what is left, and when it resets. Requires
        `account:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Usage
        """
        return (
            self.with_raw_response.get(
                talki_version=talki_version,
            )
        ).parse()

    def get_history(
        self,
        *,
        from_: None | str | Unset = UNSET,
        to: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> UsageHistory:
        """Retrieve usage history

         Return the talk time billed in each calendar month, up to 13 months, oldest first. A call counts,
        whole, in the month it was answered in. Requires `account:read`. Limited to 600 requests per minute
        per account (API key) or per installation (OAuth).

        Args:
            from_ (None | str | Unset): First month, `YYYY-MM`. Default: 12 months before `to`.
            to (None | str | Unset): Last month, included, `YYYY-MM`. Default: the current month,
                which is still counting. Not after the current month. At most 13 months from `from`.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            UsageHistory
        """
        return (
            self.with_raw_response.get_history(
                from_=from_,
                to=to,
                talki_version=talki_version,
            )
        ).parse()


class AsyncUsageResourceWithRawResponse(_resource.Resource):
    """`talki.usage.with_raw_response` on `AsyncTalki`: the methods of `talki.usage`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def get(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[Usage]:
        """`talki.usage.get`, returning the whole answer."""
        return _resource.raw(
            await get_usage.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )

    async def get_history(
        self,
        *,
        from_: None | str | Unset = UNSET,
        to: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[UsageHistory]:
        """`talki.usage.get_history`, returning the whole answer."""
        return _resource.raw(
            await get_usage_history.asyncio_detailed(
                client=self._client,
                from_=from_,
                to=to,
                talki_version=talki_version,
            )
        )


class AsyncUsageResource(_resource.Resource):
    """`talki.usage` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncUsageResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncUsageResourceWithRawResponse(self._client)

    async def get(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> Usage:
        """Retrieve usage

         Return the talk time used in the current period, what is left, and when it resets. Requires
        `account:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Usage
        """
        return (
            await self.with_raw_response.get(
                talki_version=talki_version,
            )
        ).parse()

    async def get_history(
        self,
        *,
        from_: None | str | Unset = UNSET,
        to: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> UsageHistory:
        """Retrieve usage history

         Return the talk time billed in each calendar month, up to 13 months, oldest first. A call counts,
        whole, in the month it was answered in. Requires `account:read`. Limited to 600 requests per minute
        per account (API key) or per installation (OAuth).

        Args:
            from_ (None | str | Unset): First month, `YYYY-MM`. Default: 12 months before `to`.
            to (None | str | Unset): Last month, included, `YYYY-MM`. Default: the current month,
                which is still counting. Not after the current month. At most 13 months from `from`.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            UsageHistory
        """
        return (
            await self.with_raw_response.get_history(
                from_=from_,
                to=to,
                talki_version=talki_version,
            )
        ).parse()
