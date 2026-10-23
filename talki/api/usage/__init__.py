"""The `usage` operations, one module each, and `UsageResource` / `AsyncUsageResource`,
which `Talki` and `AsyncTalki` expose as `usage`."""

from ... import _resource
from ...models.usage import Usage
from ...models.usage_history import UsageHistory
from ...types import UNSET, Unset
from . import (
    get_usage,
    get_usage_history,
)

__all__ = ["AsyncUsageResource", "UsageResource"]


class UsageResource(_resource.Resource):
    """`talki.usage`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

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
        return _resource.unwrap(
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
        return _resource.unwrap(
            get_usage_history.sync_detailed(
                client=self._client,
                from_=from_,
                to=to,
                talki_version=talki_version,
            )
        )


class AsyncUsageResource(_resource.Resource):
    """`talki.usage` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

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
        return _resource.unwrap(
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
        return _resource.unwrap(
            await get_usage_history.asyncio_detailed(
                client=self._client,
                from_=from_,
                to=to,
                talki_version=talki_version,
            )
        )
