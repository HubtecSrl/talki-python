"""The `tags` operations, one module each, and `TagsResource` / `AsyncTagsResource`,
which `Talki` and `AsyncTalki` expose as `tags`."""

from ... import _resource
from ...models.tag import Tag
from ...models.tag_create import TagCreate
from ...models.tag_list import TagList
from ...models.tag_update import TagUpdate
from ...types import UNSET, Unset
from . import (
    create_tag,
    delete_tag,
    list_tags,
    tag_contact,
    untag_contact,
    update_tag,
)

__all__ = ["AsyncTagsResource", "TagsResource"]


class TagsResource(_resource.Resource):
    """`talki.tags`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    def create(
        self,
        *,
        body: TagCreate,
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
        return _resource.unwrap(
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
        _resource.unwrap(
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
        return _resource.unwrap(
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
        return _resource.unwrap(
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
        body: TagUpdate,
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
        return _resource.unwrap(
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
        return _resource.unwrap(
            list_tags.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class AsyncTagsResource(_resource.Resource):
    """`talki.tags` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    async def create(
        self,
        *,
        body: TagCreate,
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
        return _resource.unwrap(
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
        _resource.unwrap(
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
        return _resource.unwrap(
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
        return _resource.unwrap(
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
        body: TagUpdate,
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
        return _resource.unwrap(
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
        return _resource.unwrap(
            await list_tags.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )
