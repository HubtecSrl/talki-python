"""The `whatsapp` operations, one module each, and `WhatsappResource` / `AsyncWhatsappResource`,
which `Talki` and `AsyncTalki` expose as `whatsapp`."""

from functools import cached_property

from ... import _resource
from ... import pagination as _pagination
from ...models.whats_app import WhatsApp
from ...models.whats_app_contact_rule import WhatsAppContactRule
from ...models.whats_app_contact_rule_create import WhatsAppContactRuleCreate, WhatsAppContactRuleCreateDict
from ...models.whats_app_contact_rule_list import WhatsAppContactRuleList
from ...models.whats_app_contact_rule_update import WhatsAppContactRuleUpdate, WhatsAppContactRuleUpdateDict
from ...models.whats_app_conversation import WhatsAppConversation
from ...models.whats_app_conversation_answer import WhatsAppConversationAnswer, WhatsAppConversationAnswerDict
from ...models.whats_app_conversation_list import WhatsAppConversationList
from ...models.whats_app_conversation_messages import WhatsAppConversationMessages
from ...models.whats_app_rule import WhatsAppRule
from ...models.whats_app_update import WhatsAppUpdate, WhatsAppUpdateDict
from ...types import UNSET, Unset
from . import (
    answer_whatsapp_conversation,
    create_whatsapp_contact_rule,
    delete_whatsapp_contact_rule,
    delete_whatsapp_conversations,
    get_whatsapp,
    get_whatsapp_conversation,
    get_whatsapp_conversation_messages,
    list_whatsapp_contact_rules,
    list_whatsapp_conversations,
    update_whatsapp,
    update_whatsapp_contact_rule,
)

__all__ = [
    "AsyncWhatsappResource",
    "AsyncWhatsappResourceWithRawResponse",
    "WhatsappResource",
    "WhatsappResourceWithRawResponse",
]


class WhatsappResourceWithRawResponse(_resource.Resource):
    """`talki.whatsapp.with_raw_response`: the methods of `talki.whatsapp`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def answer_conversation(
        self,
        conversation_id: str,
        *,
        body: WhatsAppConversationAnswer | WhatsAppConversationAnswerDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsAppConversation]:
        """`talki.whatsapp.answer_conversation`, returning the whole answer."""
        body = _resource.as_body(body, WhatsAppConversationAnswer)
        return _resource.raw(
            answer_whatsapp_conversation.sync_detailed(
                client=self._client,
                conversation_id=conversation_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def create_contact_rule(
        self,
        *,
        body: WhatsAppContactRuleCreate | WhatsAppContactRuleCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsAppContactRule]:
        """`talki.whatsapp.create_contact_rule`, returning the whole answer."""
        body = _resource.as_body(body, WhatsAppContactRuleCreate)
        return _resource.raw(
            create_whatsapp_contact_rule.sync_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def delete_contact_rule(
        self,
        rule_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.whatsapp.delete_contact_rule`, returning the whole answer."""
        return _resource.raw(
            delete_whatsapp_contact_rule.sync_detailed(
                client=self._client,
                rule_id=rule_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def delete_conversations(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.whatsapp.delete_conversations`, returning the whole answer."""
        return _resource.raw(
            delete_whatsapp_conversations.sync_detailed(
                client=self._client,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def get(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsApp]:
        """`talki.whatsapp.get`, returning the whole answer."""
        return _resource.raw(
            get_whatsapp.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )

    def get_conversation(
        self,
        conversation_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsAppConversation]:
        """`talki.whatsapp.get_conversation`, returning the whole answer."""
        return _resource.raw(
            get_whatsapp_conversation.sync_detailed(
                client=self._client,
                conversation_id=conversation_id,
                talki_version=talki_version,
            )
        )

    def get_conversation_messages(
        self,
        conversation_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsAppConversationMessages]:
        """`talki.whatsapp.get_conversation_messages`, returning the whole answer."""
        return _resource.raw(
            get_whatsapp_conversation_messages.sync_detailed(
                client=self._client,
                conversation_id=conversation_id,
                talki_version=talki_version,
            )
        )

    def list_contact_rules(
        self,
        *,
        rule: None | Unset | WhatsAppRule = UNSET,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.Page[WhatsAppContactRule]]:
        """`talki.whatsapp.list_contact_rules`, returning the whole answer."""

        def fetch(cursor: None | str | Unset) -> WhatsAppContactRuleList:
            return _resource.unwrap(
                list_whatsapp_contact_rules.sync_detailed(
                    client=self._client,
                    rule=rule,
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            list_whatsapp_contact_rules.sync_detailed(
                client=self._client,
                rule=rule,
                limit=limit,
                cursor=cursor,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.Page(page, fetch, cursor))

    def list_conversations(
        self,
        *,
        needs_answer: bool | Unset = False,
        limit: int | Unset = 30,
        cursor: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.Page[WhatsAppConversation]]:
        """`talki.whatsapp.list_conversations`, returning the whole answer."""

        def fetch(cursor: None | str | Unset) -> WhatsAppConversationList:
            return _resource.unwrap(
                list_whatsapp_conversations.sync_detailed(
                    client=self._client,
                    needs_answer=needs_answer,
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            list_whatsapp_conversations.sync_detailed(
                client=self._client,
                needs_answer=needs_answer,
                limit=limit,
                cursor=cursor,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.Page(page, fetch, cursor))

    def update(
        self,
        *,
        body: WhatsAppUpdate | WhatsAppUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsApp]:
        """`talki.whatsapp.update`, returning the whole answer."""
        body = _resource.as_body(body, WhatsAppUpdate)
        return _resource.raw(
            update_whatsapp.sync_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def update_contact_rule(
        self,
        rule_id: str,
        *,
        body: WhatsAppContactRuleUpdate | WhatsAppContactRuleUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsAppContactRule]:
        """`talki.whatsapp.update_contact_rule`, returning the whole answer."""
        body = _resource.as_body(body, WhatsAppContactRuleUpdate)
        return _resource.raw(
            update_whatsapp_contact_rule.sync_detailed(
                client=self._client,
                rule_id=rule_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )


class WhatsappResource(_resource.Resource):
    """`talki.whatsapp`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> WhatsappResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return WhatsappResourceWithRawResponse(self._client)

    def answer_conversation(
        self,
        conversation_id: str,
        *,
        body: WhatsAppConversationAnswer | WhatsAppConversationAnswerDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> WhatsAppConversation:
        """Answer «è un cliente?»

         Answer for the owner about the conversation's contact: `customer` (Talki answers them, now if
        WhatsApp's 24-hour window is open), `ignore` (never), or `owner` (the owner replies). Allowed on any
        conversation, asked or not. Requires `whatsapp:write`. Limited to 120 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            conversation_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (WhatsAppConversationAnswer | WhatsAppConversationAnswerDict): The owner's answer to «è un cliente?».

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsAppConversation
        """
        return (
            self.with_raw_response.answer_conversation(
                conversation_id=conversation_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def create_contact_rule(
        self,
        *,
        body: WhatsAppContactRuleCreate | WhatsAppContactRuleCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> WhatsAppContactRule:
        """Add a WhatsApp contact rule

         Add a rule for a number. A number holds one rule: change it with `PATCH`. Requires `Idempotency-
        Key`. Requires `whatsapp:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth), and to 20 creations per minute shared by the services, resources, tags, caller
        rules and WhatsApp contact rules you create.

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (WhatsAppContactRuleCreate | WhatsAppContactRuleCreateDict): A rule for a number.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsAppContactRule
        """
        return (
            self.with_raw_response.create_contact_rule(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def delete_contact_rule(
        self,
        rule_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a WhatsApp contact rule

         Remove a rule. The contact goes back to Talki's own judgement. Requires `whatsapp:write`. Limited to
        120 requests per minute per account (API key) or per installation (OAuth).

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
            self.with_raw_response.delete_contact_rule(
                rule_id=rule_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def delete_conversations(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete the stored WhatsApp chats

         Delete every stored conversation and its messages. Refused while Talki answers the chats
        (`whatsapp_answers_on`): set `mode` to `off` first. The contact rules, the appointments booked in a
        chat and the requests it left stay. Not in test mode. Requires `whatsapp:delete`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            self.with_raw_response.delete_conversations(
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def get(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> WhatsApp:
        """Retrieve the WhatsApp settings

         Return the connected WhatsApp Business number and how Talki answers its chats: the mode, the
        schedule, the conversations used this period and the owner's open questions. Requires
        `whatsapp:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsApp
        """
        return (
            self.with_raw_response.get(
                talki_version=talki_version,
            )
        ).parse()

    def get_conversation(
        self,
        conversation_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> WhatsAppConversation:
        """Retrieve a WhatsApp conversation

         Return one conversation: who wrote, its summary and outcome, and the owner's question about the
        contact. Requires `whatsapp:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            conversation_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsAppConversation
        """
        return (
            self.with_raw_response.get_conversation(
                conversation_id=conversation_id,
                talki_version=talki_version,
            )
        ).parse()

    def get_conversation_messages(
        self,
        conversation_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> WhatsAppConversationMessages:
        """Retrieve a WhatsApp conversation's messages

         Return the messages of one conversation, oldest first. `whatsapp:read` does not grant them: the
        account owner ticks `transcripts:read` on its own. Messages are kept 30 days. Requires
        `transcripts:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            conversation_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsAppConversationMessages
        """
        return (
            self.with_raw_response.get_conversation_messages(
                conversation_id=conversation_id,
                talki_version=talki_version,
            )
        ).parse()

    def list_contact_rules(
        self,
        *,
        rule: None | Unset | WhatsAppRule = UNSET,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[WhatsAppContactRule]:
        """List WhatsApp contact rules

         Return the contacts Talki never answers (`ignore`) or answers as customers (`customer`), newest
        first. Requires `whatsapp:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            rule (None | Unset | WhatsAppRule): Only `ignore` or only `customer` rules. Omit for both.
            limit (int | Unset): Maximum number of rules to return. Default: 50.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Page[WhatsAppContactRule]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """
        return (
            self.with_raw_response.list_contact_rules(
                rule=rule,
                limit=limit,
                cursor=cursor,
                talki_version=talki_version,
            )
        ).parse()

    def list_conversations(
        self,
        *,
        needs_answer: bool | Unset = False,
        limit: int | Unset = 30,
        cursor: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.Page[WhatsAppConversation]:
        """List WhatsApp conversations

         Return the conversations Talki took part in or kept out of, newest first. `needs_answer=true` lists
        those waiting for the owner's «è un cliente?». Requires `whatsapp:read`. Limited to 600 requests per
        minute per account (API key) or per installation (OAuth).

        Args:
            needs_answer (bool | Unset): Only the conversations whose «è un cliente?» waits for the
                owner's answer. Default: False.
            limit (int | Unset): Maximum number of conversations to return. Default: 30.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Page[WhatsAppConversation]: This page. Iterating it yields every row from here on,
            fetching the pages after it as it goes.
        """
        return (
            self.with_raw_response.list_conversations(
                needs_answer=needs_answer,
                limit=limit,
                cursor=cursor,
                talki_version=talki_version,
            )
        ).parse()

    def update(
        self,
        *,
        body: WhatsAppUpdate | WhatsAppUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> WhatsApp:
        """Update the WhatsApp settings

         Change the mode, the schedule, or both. Turning the answers on from `off` is refused without a plan
        that includes WhatsApp chats (`plan_feature_unavailable`), without a connected number
        (`whatsapp_not_connected`), or while Talki does not answer WhatsApp chats for any account yet
        (`whatsapp_chats_unavailable`; `blocked_reason` is `disabled`). Set the contact rules first: from
        then on Talki answers whoever writes, apart from the contacts it judges personal. Requires
        `whatsapp:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (WhatsAppUpdate | WhatsAppUpdateDict): A change of the mode, the schedule, or both. Omitted fields stay
                unchanged.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsApp
        """
        return (
            self.with_raw_response.update(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def update_contact_rule(
        self,
        rule_id: str,
        *,
        body: WhatsAppContactRuleUpdate | WhatsAppContactRuleUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> WhatsAppContactRule:
        """Update a WhatsApp contact rule

         Change a rule from `ignore` to `customer` or back. Requires `whatsapp:write`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            rule_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (WhatsAppContactRuleUpdate | WhatsAppContactRuleUpdateDict): A rule's new value.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsAppContactRule
        """
        return (
            self.with_raw_response.update_contact_rule(
                rule_id=rule_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()


class AsyncWhatsappResourceWithRawResponse(_resource.Resource):
    """`talki.whatsapp.with_raw_response` on `AsyncTalki`: the methods of `talki.whatsapp`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def answer_conversation(
        self,
        conversation_id: str,
        *,
        body: WhatsAppConversationAnswer | WhatsAppConversationAnswerDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsAppConversation]:
        """`talki.whatsapp.answer_conversation`, returning the whole answer."""
        body = _resource.as_body(body, WhatsAppConversationAnswer)
        return _resource.raw(
            await answer_whatsapp_conversation.asyncio_detailed(
                client=self._client,
                conversation_id=conversation_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def create_contact_rule(
        self,
        *,
        body: WhatsAppContactRuleCreate | WhatsAppContactRuleCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsAppContactRule]:
        """`talki.whatsapp.create_contact_rule`, returning the whole answer."""
        body = _resource.as_body(body, WhatsAppContactRuleCreate)
        return _resource.raw(
            await create_whatsapp_contact_rule.asyncio_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def delete_contact_rule(
        self,
        rule_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.whatsapp.delete_contact_rule`, returning the whole answer."""
        return _resource.raw(
            await delete_whatsapp_contact_rule.asyncio_detailed(
                client=self._client,
                rule_id=rule_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def delete_conversations(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.whatsapp.delete_conversations`, returning the whole answer."""
        return _resource.raw(
            await delete_whatsapp_conversations.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def get(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsApp]:
        """`talki.whatsapp.get`, returning the whole answer."""
        return _resource.raw(
            await get_whatsapp.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )

    async def get_conversation(
        self,
        conversation_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsAppConversation]:
        """`talki.whatsapp.get_conversation`, returning the whole answer."""
        return _resource.raw(
            await get_whatsapp_conversation.asyncio_detailed(
                client=self._client,
                conversation_id=conversation_id,
                talki_version=talki_version,
            )
        )

    async def get_conversation_messages(
        self,
        conversation_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsAppConversationMessages]:
        """`talki.whatsapp.get_conversation_messages`, returning the whole answer."""
        return _resource.raw(
            await get_whatsapp_conversation_messages.asyncio_detailed(
                client=self._client,
                conversation_id=conversation_id,
                talki_version=talki_version,
            )
        )

    async def list_contact_rules(
        self,
        *,
        rule: None | Unset | WhatsAppRule = UNSET,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.AsyncPage[WhatsAppContactRule]]:
        """`talki.whatsapp.list_contact_rules`, returning the whole answer."""

        async def fetch(cursor: None | str | Unset) -> WhatsAppContactRuleList:
            return _resource.unwrap(
                await list_whatsapp_contact_rules.asyncio_detailed(
                    client=self._client,
                    rule=rule,
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            await list_whatsapp_contact_rules.asyncio_detailed(
                client=self._client,
                rule=rule,
                limit=limit,
                cursor=cursor,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.AsyncPage(page, fetch, cursor))

    async def list_conversations(
        self,
        *,
        needs_answer: bool | Unset = False,
        limit: int | Unset = 30,
        cursor: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[_pagination.AsyncPage[WhatsAppConversation]]:
        """`talki.whatsapp.list_conversations`, returning the whole answer."""

        async def fetch(cursor: None | str | Unset) -> WhatsAppConversationList:
            return _resource.unwrap(
                await list_whatsapp_conversations.asyncio_detailed(
                    client=self._client,
                    needs_answer=needs_answer,
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            )

        return _resource.raw(
            await list_whatsapp_conversations.asyncio_detailed(
                client=self._client,
                needs_answer=needs_answer,
                limit=limit,
                cursor=cursor,
                talki_version=talki_version,
            )
        ).map(lambda page: _pagination.AsyncPage(page, fetch, cursor))

    async def update(
        self,
        *,
        body: WhatsAppUpdate | WhatsAppUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsApp]:
        """`talki.whatsapp.update`, returning the whole answer."""
        body = _resource.as_body(body, WhatsAppUpdate)
        return _resource.raw(
            await update_whatsapp.asyncio_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def update_contact_rule(
        self,
        rule_id: str,
        *,
        body: WhatsAppContactRuleUpdate | WhatsAppContactRuleUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[WhatsAppContactRule]:
        """`talki.whatsapp.update_contact_rule`, returning the whole answer."""
        body = _resource.as_body(body, WhatsAppContactRuleUpdate)
        return _resource.raw(
            await update_whatsapp_contact_rule.asyncio_detailed(
                client=self._client,
                rule_id=rule_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )


class AsyncWhatsappResource(_resource.Resource):
    """`talki.whatsapp` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncWhatsappResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncWhatsappResourceWithRawResponse(self._client)

    async def answer_conversation(
        self,
        conversation_id: str,
        *,
        body: WhatsAppConversationAnswer | WhatsAppConversationAnswerDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> WhatsAppConversation:
        """Answer «è un cliente?»

         Answer for the owner about the conversation's contact: `customer` (Talki answers them, now if
        WhatsApp's 24-hour window is open), `ignore` (never), or `owner` (the owner replies). Allowed on any
        conversation, asked or not. Requires `whatsapp:write`. Limited to 120 requests per minute per
        account (API key) or per installation (OAuth).

        Args:
            conversation_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (WhatsAppConversationAnswer | WhatsAppConversationAnswerDict): The owner's answer to «è un cliente?».

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsAppConversation
        """
        return (
            await self.with_raw_response.answer_conversation(
                conversation_id=conversation_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def create_contact_rule(
        self,
        *,
        body: WhatsAppContactRuleCreate | WhatsAppContactRuleCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> WhatsAppContactRule:
        """Add a WhatsApp contact rule

         Add a rule for a number. A number holds one rule: change it with `PATCH`. Requires `Idempotency-
        Key`. Requires `whatsapp:write`. Limited to 120 requests per minute per account (API key) or per
        installation (OAuth), and to 20 creations per minute shared by the services, resources, tags, caller
        rules and WhatsApp contact rules you create.

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (WhatsAppContactRuleCreate | WhatsAppContactRuleCreateDict): A rule for a number.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsAppContactRule
        """
        return (
            await self.with_raw_response.create_contact_rule(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def delete_contact_rule(
        self,
        rule_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a WhatsApp contact rule

         Remove a rule. The contact goes back to Talki's own judgement. Requires `whatsapp:write`. Limited to
        120 requests per minute per account (API key) or per installation (OAuth).

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
            await self.with_raw_response.delete_contact_rule(
                rule_id=rule_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def delete_conversations(
        self,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete the stored WhatsApp chats

         Delete every stored conversation and its messages. Refused while Talki answers the chats
        (`whatsapp_answers_on`): set `mode` to `off` first. The contact rules, the appointments booked in a
        chat and the requests it left stay. Not in test mode. Requires `whatsapp:delete`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            None
        """
        (
            await self.with_raw_response.delete_conversations(
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def get(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> WhatsApp:
        """Retrieve the WhatsApp settings

         Return the connected WhatsApp Business number and how Talki answers its chats: the mode, the
        schedule, the conversations used this period and the owner's open questions. Requires
        `whatsapp:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsApp
        """
        return (
            await self.with_raw_response.get(
                talki_version=talki_version,
            )
        ).parse()

    async def get_conversation(
        self,
        conversation_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> WhatsAppConversation:
        """Retrieve a WhatsApp conversation

         Return one conversation: who wrote, its summary and outcome, and the owner's question about the
        contact. Requires `whatsapp:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            conversation_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsAppConversation
        """
        return (
            await self.with_raw_response.get_conversation(
                conversation_id=conversation_id,
                talki_version=talki_version,
            )
        ).parse()

    async def get_conversation_messages(
        self,
        conversation_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> WhatsAppConversationMessages:
        """Retrieve a WhatsApp conversation's messages

         Return the messages of one conversation, oldest first. `whatsapp:read` does not grant them: the
        account owner ticks `transcripts:read` on its own. Messages are kept 30 days. Requires
        `transcripts:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            conversation_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsAppConversationMessages
        """
        return (
            await self.with_raw_response.get_conversation_messages(
                conversation_id=conversation_id,
                talki_version=talki_version,
            )
        ).parse()

    def list_contact_rules(
        self,
        *,
        rule: None | Unset | WhatsAppRule = UNSET,
        limit: int | Unset = 50,
        cursor: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPager[WhatsAppContactRule]:
        """List WhatsApp contact rules

         Return the contacts Talki never answers (`ignore`) or answers as customers (`customer`), newest
        first. Requires `whatsapp:read`. Limited to 600 requests per minute per account (API key) or per
        installation (OAuth).

        Args:
            rule (None | Unset | WhatsAppRule): Only `ignore` or only `customer` rules. Omit for both.
            limit (int | Unset): Maximum number of rules to return. Default: 50.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AsyncPager[WhatsAppContactRule]: Awaited, this page (an `AsyncPage`). Iterated with `async for`,
            every row from here on, fetching the pages as it goes.
        """

        async def first() -> _pagination.AsyncPage[WhatsAppContactRule]:
            return (
                await self.with_raw_response.list_contact_rules(
                    rule=rule,
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            ).parse()

        return _pagination.AsyncPager(first)

    def list_conversations(
        self,
        *,
        needs_answer: bool | Unset = False,
        limit: int | Unset = 30,
        cursor: None | str | Unset = UNSET,
        talki_version: str | Unset = UNSET,
    ) -> _pagination.AsyncPager[WhatsAppConversation]:
        """List WhatsApp conversations

         Return the conversations Talki took part in or kept out of, newest first. `needs_answer=true` lists
        those waiting for the owner's «è un cliente?». Requires `whatsapp:read`. Limited to 600 requests per
        minute per account (API key) or per installation (OAuth).

        Args:
            needs_answer (bool | Unset): Only the conversations whose «è un cliente?» waits for the
                owner's answer. Default: False.
            limit (int | Unset): Maximum number of conversations to return. Default: 30.
            cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`. Omit
                for the first page.
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            AsyncPager[WhatsAppConversation]: Awaited, this page (an `AsyncPage`). Iterated with `async for`,
            every row from here on, fetching the pages as it goes.
        """

        async def first() -> _pagination.AsyncPage[WhatsAppConversation]:
            return (
                await self.with_raw_response.list_conversations(
                    needs_answer=needs_answer,
                    limit=limit,
                    cursor=cursor,
                    talki_version=talki_version,
                )
            ).parse()

        return _pagination.AsyncPager(first)

    async def update(
        self,
        *,
        body: WhatsAppUpdate | WhatsAppUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> WhatsApp:
        """Update the WhatsApp settings

         Change the mode, the schedule, or both. Turning the answers on from `off` is refused without a plan
        that includes WhatsApp chats (`plan_feature_unavailable`), without a connected number
        (`whatsapp_not_connected`), or while Talki does not answer WhatsApp chats for any account yet
        (`whatsapp_chats_unavailable`; `blocked_reason` is `disabled`). Set the contact rules first: from
        then on Talki answers whoever writes, apart from the contacts it judges personal. Requires
        `whatsapp:write`. Limited to 120 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (WhatsAppUpdate | WhatsAppUpdateDict): A change of the mode, the schedule, or both. Omitted fields stay
                unchanged.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsApp
        """
        return (
            await self.with_raw_response.update(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def update_contact_rule(
        self,
        rule_id: str,
        *,
        body: WhatsAppContactRuleUpdate | WhatsAppContactRuleUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> WhatsAppContactRule:
        """Update a WhatsApp contact rule

         Change a rule from `ignore` to `customer` or back. Requires `whatsapp:write`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            rule_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (WhatsAppContactRuleUpdate | WhatsAppContactRuleUpdateDict): A rule's new value.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            WhatsAppContactRule
        """
        return (
            await self.with_raw_response.update_contact_rule(
                rule_id=rule_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()
