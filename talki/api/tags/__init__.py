"""The `tags` operations, one module each, and `TagsResource` / `AsyncTagsResource`,
which `Talki` and `AsyncTalki` expose as `tags`."""

from functools import cached_property

from ... import _resource
from ...models.tag import Tag
from ...models.tag_create import TagCreate, TagCreateDict
from ...models.tag_list import TagList
from ...models.tag_update import TagUpdate, TagUpdateDict
from ...types import UNSET, Unset
from . import (
    create_tag,
    delete_tag,
    list_tags,
    tag_contact,
    untag_contact,
    update_tag,
)

__all__ = [
    "AsyncTagsResource",
    "AsyncTagsResourceWithRawResponse",
    "TagsResource",
    "TagsResourceWithRawResponse",
]


class TagsResourceWithRawResponse(_resource.Resource):
    """`talki.tags.with_raw_response`: the methods of `talki.tags`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def create(
        self,
        *,
        body: TagCreate | TagCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Tag]:
        """`talki.tags.create`, returning the whole answer."""
        body = _resource.as_body(body, TagCreate)
        return _resource.raw(
            create_tag.sync_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def delete(
        self,
        tag_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.tags.delete`, returning the whole answer."""
        return _resource.raw(
            delete_tag.sync_detailed(
                client=self._client,
                tag_id=tag_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def tag_contact(
        self,
        tag_id: str,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Tag]:
        """`talki.tags.tag_contact`, returning the whole answer."""
        return _resource.raw(
            tag_contact.sync_detailed(
                client=self._client,
                tag_id=tag_id,
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def untag_contact(
        self,
        tag_id: str,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Tag]:
        """`talki.tags.untag_contact`, returning the whole answer."""
        return _resource.raw(
            untag_contact.sync_detailed(
                client=self._client,
                tag_id=tag_id,
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def update(
        self,
        tag_id: str,
        *,
        body: TagUpdate | TagUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Tag]:
        """`talki.tags.update`, returning the whole answer."""
        body = _resource.as_body(body, TagUpdate)
        return _resource.raw(
            update_tag.sync_detailed(
                client=self._client,
                tag_id=tag_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[TagList]:
        """`talki.tags.list`, returning the whole answer."""
        return _resource.raw(
            list_tags.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class TagsResource(_resource.Resource):
    """`talki.tags`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> TagsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return TagsResourceWithRawResponse(self._client)

    def create(
        self,
        *,
        body: TagCreate | TagCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Tag:
        """Create a tag

         Create a tag. An account holds at most 50. Requires `Idempotency-Key`. Requires `contacts:write`.
        Limited to 120 requests per minute per account (API key) or per installation (OAuth), and to 20
        creations per minute shared by the services, resources, tags and caller rules you create.

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (TagCreate): A new tag. An account holds at most 50.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Tag
        """
        return (
            self.with_raw_response.create(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def delete(
        self,
        tag_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a tag

         Delete a tag. The contacts it was on are not affected. Requires `contacts:write`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            tag_id (str):
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
                tag_id=tag_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def tag_contact(
        self,
        tag_id: str,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Tag:
        """Tag a contact

         Put a tag on a contact. Idempotent. Requires `contacts:write`. Limited to 120 requests per minute
        per account (API key) or per installation (OAuth).

        Args:
            tag_id (str):
            contact_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Tag
        """
        return (
            self.with_raw_response.tag_contact(
                tag_id=tag_id,
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def untag_contact(
        self,
        tag_id: str,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Tag:
        """Untag a contact

         Take a tag off a contact and return the tag. Idempotent. Requires `contacts:write`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            tag_id (str):
            contact_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Tag
        """
        return (
            self.with_raw_response.untag_contact(
                tag_id=tag_id,
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def update(
        self,
        tag_id: str,
        *,
        body: TagUpdate | TagUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Tag:
        """Update a tag

         Rename or recolour a tag. Requires `contacts:write`. Limited to 120 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            tag_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (TagUpdate): A partial edit of a tag.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Tag
        """
        return (
            self.with_raw_response.update(
                tag_id=tag_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> TagList:
        """List tags

         Return every tag with the contacts that carry it. Requires `contacts:read`. Limited to 600 requests
        per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            TagList
        """
        return (
            self.with_raw_response.list(
                talki_version=talki_version,
            )
        ).parse()


class AsyncTagsResourceWithRawResponse(_resource.Resource):
    """`talki.tags.with_raw_response` on `AsyncTalki`: the methods of `talki.tags`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def create(
        self,
        *,
        body: TagCreate | TagCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Tag]:
        """`talki.tags.create`, returning the whole answer."""
        body = _resource.as_body(body, TagCreate)
        return _resource.raw(
            await create_tag.asyncio_detailed(
                client=self._client,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def delete(
        self,
        tag_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[None]:
        """`talki.tags.delete`, returning the whole answer."""
        return _resource.raw(
            await delete_tag.asyncio_detailed(
                client=self._client,
                tag_id=tag_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def tag_contact(
        self,
        tag_id: str,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Tag]:
        """`talki.tags.tag_contact`, returning the whole answer."""
        return _resource.raw(
            await tag_contact.asyncio_detailed(
                client=self._client,
                tag_id=tag_id,
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def untag_contact(
        self,
        tag_id: str,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Tag]:
        """`talki.tags.untag_contact`, returning the whole answer."""
        return _resource.raw(
            await untag_contact.asyncio_detailed(
                client=self._client,
                tag_id=tag_id,
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def update(
        self,
        tag_id: str,
        *,
        body: TagUpdate | TagUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> _resource.RawResponse[Tag]:
        """`talki.tags.update`, returning the whole answer."""
        body = _resource.as_body(body, TagUpdate)
        return _resource.raw(
            await update_tag.asyncio_detailed(
                client=self._client,
                tag_id=tag_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        )

    async def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[TagList]:
        """`talki.tags.list`, returning the whole answer."""
        return _resource.raw(
            await list_tags.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class AsyncTagsResource(_resource.Resource):
    """`talki.tags` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncTagsResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncTagsResourceWithRawResponse(self._client)

    async def create(
        self,
        *,
        body: TagCreate | TagCreateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Tag:
        """Create a tag

         Create a tag. An account holds at most 50. Requires `Idempotency-Key`. Requires `contacts:write`.
        Limited to 120 requests per minute per account (API key) or per installation (OAuth), and to 20
        creations per minute shared by the services, resources, tags and caller rules you create.

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
                unless the client adds one, as `Talki` and `AsyncTalki` do unless built with
                `auto_idempotency=False`.
            body (TagCreate): A new tag. An account holds at most 50.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Tag
        """
        return (
            await self.with_raw_response.create(
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def delete(
        self,
        tag_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> None:
        """Delete a tag

         Delete a tag. The contacts it was on are not affected. Requires `contacts:write`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            tag_id (str):
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
                tag_id=tag_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def tag_contact(
        self,
        tag_id: str,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Tag:
        """Tag a contact

         Put a tag on a contact. Idempotent. Requires `contacts:write`. Limited to 120 requests per minute
        per account (API key) or per installation (OAuth).

        Args:
            tag_id (str):
            contact_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Tag
        """
        return (
            await self.with_raw_response.tag_contact(
                tag_id=tag_id,
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def untag_contact(
        self,
        tag_id: str,
        contact_id: str,
        *,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Tag:
        """Untag a contact

         Take a tag off a contact and return the tag. Idempotent. Requires `contacts:write`. Limited to 120
        requests per minute per account (API key) or per installation (OAuth).

        Args:
            tag_id (str):
            contact_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Tag
        """
        return (
            await self.with_raw_response.untag_contact(
                tag_id=tag_id,
                contact_id=contact_id,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def update(
        self,
        tag_id: str,
        *,
        body: TagUpdate | TagUpdateDict,
        talki_version: str | Unset = UNSET,
        idempotency_key: str | Unset = UNSET,
    ) -> Tag:
        """Update a tag

         Rename or recolour a tag. Requires `contacts:write`. Limited to 120 requests per minute per account
        (API key) or per installation (OAuth).

        Args:
            tag_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.
            idempotency_key (str | Unset):
            body (TagUpdate): A partial edit of a tag.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            Tag
        """
        return (
            await self.with_raw_response.update(
                tag_id=tag_id,
                body=body,
                talki_version=talki_version,
                idempotency_key=idempotency_key,
            )
        ).parse()

    async def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> TagList:
        """List tags

         Return every tag with the contacts that carry it. Requires `contacts:read`. Limited to 600 requests
        per minute per account (API key) or per installation (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            TagList
        """
        return (
            await self.with_raw_response.list(
                talki_version=talki_version,
            )
        ).parse()
