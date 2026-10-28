"""The `sandbox` operations, one module each, and `SandboxResource` / `AsyncSandboxResource`,
which `Talki` and `AsyncTalki` expose as `sandbox`."""

from functools import cached_property

from ... import _resource
from ...models.fake_call_request import FakeCallRequest, FakeCallRequestDict
from ...models.fake_call_response import FakeCallResponse
from ...models.reset_response import ResetResponse
from ...models.scenario_summary import ScenarioSummary
from ...types import UNSET, Unset
from . import (
    create_sandbox_call,
    list_sandbox_scenarios,
    reset_sandbox,
)

__all__ = [
    "AsyncSandboxResource",
    "AsyncSandboxResourceWithRawResponse",
    "SandboxResource",
    "SandboxResourceWithRawResponse",
]


class SandboxResourceWithRawResponse(_resource.Resource):
    """`talki.sandbox.with_raw_response`: the methods of `talki.sandbox`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def create_call(
        self,
        *,
        body: FakeCallRequest | FakeCallRequestDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[FakeCallResponse]:
        """`talki.sandbox.create_call`, returning the whole answer."""
        body = _resource.as_body(body, FakeCallRequest)
        return _resource.raw(
            create_sandbox_call.sync_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def list_scenarios(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[list[ScenarioSummary]]:
        """`talki.sandbox.list_scenarios`, returning the whole answer."""
        return _resource.raw(
            list_sandbox_scenarios.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )

    def reset(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[ResetResponse]:
        """`talki.sandbox.reset`, returning the whole answer."""
        return _resource.raw(
            reset_sandbox.sync_detailed(
                client=self._client,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )


class SandboxResource(_resource.Resource):
    """`talki.sandbox`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> SandboxResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return SandboxResourceWithRawResponse(self._client)

    def create_call(
        self,
        *,
        body: FakeCallRequest | FakeCallRequestDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> FakeCallResponse:
        """Create a sandbox call

         Tell the sandbox it had a call. The whole post-call flow runs for real, including signed webhook
        deliveries carrying `livemode: false`. Requires a developer sandbox; answers 404 on a real account.
        Limited to 30 requests per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (FakeCallRequest | FakeCallRequestDict): The call a sandbox should pretend it had.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            FakeCallResponse
        """
        return (
            self.with_raw_response.create_call(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list_scenarios(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> list[ScenarioSummary]:
        """List sandbox scenarios

         Return the named calls this sandbox can be told it had, with the exact events each one emits.
        Requires a developer sandbox; answers 404 on a real account. Limited to 600 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            list[ScenarioSummary]
        """
        return (
            self.with_raw_response.list_scenarios(
                talki_version=talki_version,
            )
        ).parse()

    def reset(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> ResetResponse:
        """Reset the sandbox

         Delete this sandbox's history and rebuild it from a fixed seed. Credentials, installations and
        services survive. Requires a developer sandbox; answers 404 on a real account. Limited to 6 requests
        per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            ResetResponse
        """
        return (
            self.with_raw_response.reset(
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()


class AsyncSandboxResourceWithRawResponse(_resource.Resource):
    """`talki.sandbox.with_raw_response` on `AsyncTalki`: the methods of `talki.sandbox`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def create_call(
        self,
        *,
        body: FakeCallRequest | FakeCallRequestDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[FakeCallResponse]:
        """`talki.sandbox.create_call`, returning the whole answer."""
        body = _resource.as_body(body, FakeCallRequest)
        return _resource.raw(
            await create_sandbox_call.asyncio_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def list_scenarios(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[list[ScenarioSummary]]:
        """`talki.sandbox.list_scenarios`, returning the whole answer."""
        return _resource.raw(
            await list_sandbox_scenarios.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )

    async def reset(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[ResetResponse]:
        """`talki.sandbox.reset`, returning the whole answer."""
        return _resource.raw(
            await reset_sandbox.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )


class AsyncSandboxResource(_resource.Resource):
    """`talki.sandbox` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncSandboxResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncSandboxResourceWithRawResponse(self._client)

    async def create_call(
        self,
        *,
        body: FakeCallRequest | FakeCallRequestDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> FakeCallResponse:
        """Create a sandbox call

         Tell the sandbox it had a call. The whole post-call flow runs for real, including signed webhook
        deliveries carrying `livemode: false`. Requires a developer sandbox; answers 404 on a real account.
        Limited to 30 requests per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (FakeCallRequest | FakeCallRequestDict): The call a sandbox should pretend it had.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            FakeCallResponse
        """
        return (
            await self.with_raw_response.create_call(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def list_scenarios(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> list[ScenarioSummary]:
        """List sandbox scenarios

         Return the named calls this sandbox can be told it had, with the exact events each one emits.
        Requires a developer sandbox; answers 404 on a real account. Limited to 600 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            list[ScenarioSummary]
        """
        return (
            await self.with_raw_response.list_scenarios(
                talki_version=talki_version,
            )
        ).parse()

    async def reset(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> ResetResponse:
        """Reset the sandbox

         Delete this sandbox's history and rebuild it from a fixed seed. Credentials, installations and
        services survive. Requires a developer sandbox; answers 404 on a real account. Limited to 6 requests
        per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            ResetResponse
        """
        return (
            await self.with_raw_response.reset(
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()
