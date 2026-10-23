"""The `sandbox` operations, one module each, and `SandboxResource` / `AsyncSandboxResource`,
which `Talki` and `AsyncTalki` expose as `sandbox`."""

from ... import _resource
from ...models.fake_call_request import FakeCallRequest
from ...models.fake_call_response import FakeCallResponse
from ...models.reset_response import ResetResponse
from ...models.scenario_summary import ScenarioSummary
from ...types import UNSET, Unset
from . import (
    create_sandbox_call,
    list_sandbox_scenarios,
    reset_sandbox,
)

__all__ = ["AsyncSandboxResource", "SandboxResource"]


class SandboxResource(_resource.Resource):
    """`talki.sandbox`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    def create_call(
        self,
        *,
        body: FakeCallRequest,
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
            body (FakeCallRequest): The call a sandbox should pretend it had.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            FakeCallResponse
        """
        return _resource.unwrap(
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
        return _resource.unwrap(
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
        return _resource.unwrap(
            reset_sandbox.sync_detailed(
                client=self._client,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )


class AsyncSandboxResource(_resource.Resource):
    """`talki.sandbox` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    async def create_call(
        self,
        *,
        body: FakeCallRequest,
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
            body (FakeCallRequest): The call a sandbox should pretend it had.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            FakeCallResponse
        """
        return _resource.unwrap(
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
        return _resource.unwrap(
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
        return _resource.unwrap(
            await reset_sandbox.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )
