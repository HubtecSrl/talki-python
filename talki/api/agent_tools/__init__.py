"""The `agent_tools` operations, one module each, and `AgentToolsResource` / `AsyncAgentToolsResource`,
which `Talki` and `AsyncTalki` expose as `agent_tools`."""

from functools import cached_property

from ... import _resource
from ...models.agent_tools import AgentTools
from ...models.agent_tools_update import AgentToolsUpdate, AgentToolsUpdateDict
from ...types import UNSET, Unset
from . import (
    get_agent_tools,
    update_agent_tools,
)

__all__ = [
    "AsyncAgentToolsResource",
    "AsyncAgentToolsResourceWithRawResponse",
    "AgentToolsResource",
    "AgentToolsResourceWithRawResponse",
]


class AgentToolsResourceWithRawResponse(_resource.Resource):
    """`talki.agent_tools.with_raw_response`: the methods of `talki.agent_tools`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[AgentTools]:
        """`talki.agent_tools.get`, returning the whole answer."""
        return _resource.raw(
            get_agent_tools.sync_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    def update(
        self,
        *,
        body: AgentToolsUpdate | AgentToolsUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[AgentTools]:
        """`talki.agent_tools.update`, returning the whole answer."""
        body = _resource.as_body(body, AgentToolsUpdate)
        return _resource.raw(
            update_agent_tools.sync_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )


class AgentToolsResource(_resource.Resource):
    """`talki.agent_tools`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AgentToolsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AgentToolsResourceWithRawResponse(self._client)

    def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> AgentTools:
        """Retrieve the agent tools

         Return your app's tools that have an approved revision, and which of them the assistant may call on
        this account's calls: the account's list, used at every location without one of its own, or with
        `location_id` that location's list, or the account's it follows (`inherited`). Every tool starts
        off. Only your app's OAuth access token is accepted, on an installation that holds
        `agent_tools:write`, and only once Talki has enabled the app for agent tools
        (`agent_tools_not_enabled`). An API key is refused (`insufficient_scope`): it cannot hold
        `agent_tools:write`. Requires `agent_tools:write`. Limited to 600 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): A location's own list, an id from `GET /v1/locations`.
                Omit it for the account's list, used at every location without its own.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AgentTools
        """
        return (
            self.with_raw_response.get(
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()

    def update(
        self,
        *,
        body: AgentToolsUpdate | AgentToolsUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> AgentTools:
        """Update the agent tools

         Replace the list of tools the assistant may call: the account's, or with `location_id` that
        location's own, which replaces the account's there. Only tools with an approved revision can be
        switched on, and `[]` switches every tool off. `"enabled": null` with `location_id` drops the
        location's own list, so it follows the account's again; the account's list cannot be null. One call
        has at most `limit_per_call` agent tools, counted across every app the account granted
        `agent_tools:write`, those the owner switched off included: a change that raises any location's
        count above that is refused (`tool_limit`), and one that does not raise it never is. While the owner
        has switched your app's tools off (`owner_off`), the lists are kept and none of the tools reaches a
        call. Only your app's OAuth access token is accepted, as for `GET`; an API key is refused
        (`insufficient_scope`). Requires `agent_tools:write`. Limited to 120 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): A location's own list, an id from `GET /v1/locations`.
                Omit it for the account's list, used at every location without its own.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (AgentToolsUpdate | AgentToolsUpdateDict): The list of tools to switch on, replacing the one stored at this
                level.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AgentTools
        """
        return (
            self.with_raw_response.update(
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()


class AsyncAgentToolsResourceWithRawResponse(_resource.Resource):
    """`talki.agent_tools.with_raw_response` on `AsyncTalki`: the methods of `talki.agent_tools`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[AgentTools]:
        """`talki.agent_tools.get`, returning the whole answer."""
        return _resource.raw(
            await get_agent_tools.asyncio_detailed(
                client=self._client,
                location_id=location_id,
                talki_version=talki_version,
            )
        )

    async def update(
        self,
        *,
        body: AgentToolsUpdate | AgentToolsUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[AgentTools]:
        """`talki.agent_tools.update`, returning the whole answer."""
        body = _resource.as_body(body, AgentToolsUpdate)
        return _resource.raw(
            await update_agent_tools.asyncio_detailed(
                client=self._client,
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )


class AsyncAgentToolsResource(_resource.Resource):
    """`talki.agent_tools` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncAgentToolsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncAgentToolsResourceWithRawResponse(self._client)

    async def get(
        self,
        *,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> AgentTools:
        """Retrieve the agent tools

         Return your app's tools that have an approved revision, and which of them the assistant may call on
        this account's calls: the account's list, used at every location without one of its own, or with
        `location_id` that location's list, or the account's it follows (`inherited`). Every tool starts
        off. Only your app's OAuth access token is accepted, on an installation that holds
        `agent_tools:write`, and only once Talki has enabled the app for agent tools
        (`agent_tools_not_enabled`). An API key is refused (`insufficient_scope`): it cannot hold
        `agent_tools:write`. Requires `agent_tools:write`. Limited to 600 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): A location's own list, an id from `GET /v1/locations`.
                Omit it for the account's list, used at every location without its own.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AgentTools
        """
        return (
            await self.with_raw_response.get(
                location_id=location_id,
                talki_version=talki_version,
            )
        ).parse()

    async def update(
        self,
        *,
        body: AgentToolsUpdate | AgentToolsUpdateDict,
        location_id: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> AgentTools:
        """Update the agent tools

         Replace the list of tools the assistant may call: the account's, or with `location_id` that
        location's own, which replaces the account's there. Only tools with an approved revision can be
        switched on, and `[]` switches every tool off. `"enabled": null` with `location_id` drops the
        location's own list, so it follows the account's again; the account's list cannot be null. One call
        has at most `limit_per_call` agent tools, counted across every app the account granted
        `agent_tools:write`, those the owner switched off included: a change that raises any location's
        count above that is refused (`tool_limit`), and one that does not raise it never is. While the owner
        has switched your app's tools off (`owner_off`), the lists are kept and none of the tools reaches a
        call. Only your app's OAuth access token is accepted, as for `GET`; an API key is refused
        (`insufficient_scope`). Requires `agent_tools:write`. Limited to 120 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            location_id (None | str | Unset): A location's own list, an id from `GET /v1/locations`.
                Omit it for the account's list, used at every location without its own.
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (AgentToolsUpdate | AgentToolsUpdateDict): The list of tools to switch on, replacing the one stored at this
                level.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AgentTools
        """
        return (
            await self.with_raw_response.update(
                body=body,
                location_id=location_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()
