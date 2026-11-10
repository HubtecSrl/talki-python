"""The `agent_test` operations, one module each, and `AgentTestResource` / `AsyncAgentTestResource`,
which `Talki` and `AsyncTalki` expose as `agent_test`."""

from functools import cached_property

from ... import _resource
from ...models.agent_test_message import AgentTestMessage, AgentTestMessageDict
from ...models.agent_test_reply import AgentTestReply
from ...types import UNSET, Unset
from . import (
    end_agent_test,
    send_agent_test,
)

__all__ = [
    "AsyncAgentTestResource",
    "AsyncAgentTestResourceWithRawResponse",
    "AgentTestResource",
    "AgentTestResourceWithRawResponse",
]


class AgentTestResourceWithRawResponse(_resource.Resource):
    """`talki.agent_test.with_raw_response`: the methods of `talki.agent_test`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def end(
        self,
        session_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.agent_test.end`, returning the whole answer."""
        return _resource.raw(
            end_agent_test.sync_detailed(
                client=self._client,
                session_id=session_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def send(
        self,
        *,
        body: AgentTestMessage | AgentTestMessageDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[AgentTestReply]:
        """`talki.agent_test.send`, returning the whole answer."""
        body = _resource.as_body(body, AgentTestMessage)
        return _resource.raw(
            send_agent_test.sync_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )


class AgentTestResource(_resource.Resource):
    """`talki.agent_test`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AgentTestResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AgentTestResourceWithRawResponse(self._client)

    def end(
        self,
        session_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """End a test session

         Drop a test session and its history now, rather than 30 minutes after its last turn. Only the
        credential that started it can end it. Refused with `409` `request_conflict` while a message of the
        session is being answered. Requires `account:write` and `knowledge:read`. Limited to 120 requests
        per minute per account (API key) or per installation (OAuth).

        Args:
            session_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            self.with_raw_response.end(
                session_id=session_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def send(
        self,
        *,
        body: AgentTestMessage | AgentTestMessageDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> AgentTestReply:
        """Send a test message

         Send one message to the account's assistant, as a caller would say it, and return its answer: what a
        call to the location would hear, from the same settings, documents, services, calendar and partner
        tools, written as text. Nothing is saved: a booking the assistant makes is not made, and no call,
        appointment or unresolved request is recorded. The first message starts a session; send its
        `session_id` with the next ones. Talki keeps the history for 30 minutes after the last turn, and a
        session holds at most 20 turns (then `agent_test_session_full`). A session belongs to the credential
        that started it. Your app's own partner tools run, sent with `test_drive: true`, writes included; no
        other app's do. The assistant here runs on a text model, not the one that answers calls, so a reply
        can be worded differently from what a caller would hear. Refused while the managing partner has
        suspended the account (`account_suspended`). An account may send 25 test messages a day, shared with
        the test in the Talki apps, and an OAuth app 300 a day across all the accounts it is installed on;
        past either, `429` `rate_limit_exceeded` with `Retry-After`. Requires `account:write` and
        `knowledge:read`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth), and to 15 test messages per minute.

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (AgentTestMessage | AgentTestMessageDict): One message to the assistant, as a caller would say it. Omit
                `session_id` to start a session, and send the one from the reply to continue it: Talki
                keeps the history, and there is no way to send one. A session stays at the location it
                started at.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AgentTestReply
        """
        return (
            self.with_raw_response.send(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()


class AsyncAgentTestResourceWithRawResponse(_resource.Resource):
    """`talki.agent_test.with_raw_response` on `AsyncTalki`: the methods of `talki.agent_test`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def end(
        self,
        session_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.agent_test.end`, returning the whole answer."""
        return _resource.raw(
            await end_agent_test.asyncio_detailed(
                client=self._client,
                session_id=session_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def send(
        self,
        *,
        body: AgentTestMessage | AgentTestMessageDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[AgentTestReply]:
        """`talki.agent_test.send`, returning the whole answer."""
        body = _resource.as_body(body, AgentTestMessage)
        return _resource.raw(
            await send_agent_test.asyncio_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )


class AsyncAgentTestResource(_resource.Resource):
    """`talki.agent_test` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncAgentTestResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncAgentTestResourceWithRawResponse(self._client)

    async def end(
        self,
        session_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """End a test session

         Drop a test session and its history now, rather than 30 minutes after its last turn. Only the
        credential that started it can end it. Refused with `409` `request_conflict` while a message of the
        session is being answered. Requires `account:write` and `knowledge:read`. Limited to 120 requests
        per minute per account (API key) or per installation (OAuth).

        Args:
            session_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            await self.with_raw_response.end(
                session_id=session_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def send(
        self,
        *,
        body: AgentTestMessage | AgentTestMessageDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> AgentTestReply:
        """Send a test message

         Send one message to the account's assistant, as a caller would say it, and return its answer: what a
        call to the location would hear, from the same settings, documents, services, calendar and partner
        tools, written as text. Nothing is saved: a booking the assistant makes is not made, and no call,
        appointment or unresolved request is recorded. The first message starts a session; send its
        `session_id` with the next ones. Talki keeps the history for 30 minutes after the last turn, and a
        session holds at most 20 turns (then `agent_test_session_full`). A session belongs to the credential
        that started it. Your app's own partner tools run, sent with `test_drive: true`, writes included; no
        other app's do. The assistant here runs on a text model, not the one that answers calls, so a reply
        can be worded differently from what a caller would hear. Refused while the managing partner has
        suspended the account (`account_suspended`). An account may send 25 test messages a day, shared with
        the test in the Talki apps, and an OAuth app 300 a day across all the accounts it is installed on;
        past either, `429` `rate_limit_exceeded` with `Retry-After`. Requires `account:write` and
        `knowledge:read`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth), and to 15 test messages per minute.

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (AgentTestMessage | AgentTestMessageDict): One message to the assistant, as a caller would say it. Omit
                `session_id` to start a session, and send the one from the reply to continue it: Talki
                keeps the history, and there is no way to send one. A session stays at the location it
                started at.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AgentTestReply
        """
        return (
            await self.with_raw_response.send(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()
