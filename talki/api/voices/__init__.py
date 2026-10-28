"""The `voices` operations, one module each, and `VoicesResource` / `AsyncVoicesResource`,
which `Talki` and `AsyncTalki` expose as `voices`."""

from functools import cached_property

from ... import _resource
from ...models.voice_list import VoiceList
from ...types import UNSET, File, Unset
from . import (
    get_voice_preview,
    list_voices,
)

__all__ = [
    "AsyncVoicesResource",
    "AsyncVoicesResourceWithRawResponse",
    "VoicesResource",
    "VoicesResourceWithRawResponse",
]


class VoicesResourceWithRawResponse(_resource.Resource):
    """`talki.voices.with_raw_response`: the methods of `talki.voices`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    def get_preview(
        self,
        voice_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[File]:
        """`talki.voices.get_preview`, returning the whole answer."""
        return _resource.raw(
            get_voice_preview.sync_detailed(
                client=self._client,
                voice_id=voice_id,
                talki_version=talki_version,
            )
        )

    def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[VoiceList]:
        """`talki.voices.list`, returning the whole answer."""
        return _resource.raw(
            list_voices.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class VoicesResource(_resource.Resource):
    """`talki.voices`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> VoicesResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return VoicesResourceWithRawResponse(self._client)

    def get_preview(
        self,
        voice_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> File:
        """Retrieve a voice sample

         Return a short WAV sample of one voice, the same for every account. Requires `account:read`. Limited
        to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            voice_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            File
        """
        return (
            self.with_raw_response.get_preview(
                voice_id=voice_id,
                talki_version=talki_version,
            )
        ).parse()

    def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> VoiceList:
        """List voices

         Return every voice the assistant can speak with. The account's `voice` is one of these IDs. Requires
        `account:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            VoiceList
        """
        return (
            self.with_raw_response.list(
                talki_version=talki_version,
            )
        ).parse()


class AsyncVoicesResourceWithRawResponse(_resource.Resource):
    """`talki.voices.with_raw_response` on `AsyncTalki`: the methods of `talki.voices`, each
    returning the whole answer, a `talki.RawResponse` whose `parse()` is what the
    method returns. An error raises as it does there."""

    async def get_preview(
        self,
        voice_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[File]:
        """`talki.voices.get_preview`, returning the whole answer."""
        return _resource.raw(
            await get_voice_preview.asyncio_detailed(
                client=self._client,
                voice_id=voice_id,
                talki_version=talki_version,
            )
        )

    async def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> _resource.RawResponse[VoiceList]:
        """`talki.voices.list`, returning the whole answer."""
        return _resource.raw(
            await list_voices.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class AsyncVoicesResource(_resource.Resource):
    """`talki.voices` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

    @cached_property
    def with_raw_response(self) -> AsyncVoicesResourceWithRawResponse:
        """The same methods, each returning the whole answer: its status and
        headers (`ETag`, `X-Request-Id`, the rate limits) with the value."""
        return AsyncVoicesResourceWithRawResponse(self._client)

    async def get_preview(
        self,
        voice_id: str,
        *,
        talki_version: str | Unset = UNSET,
    ) -> File:
        """Retrieve a voice sample

         Return a short WAV sample of one voice, the same for every account. Requires `account:read`. Limited
        to 600 requests per minute per account (API key) or per installation (OAuth).

        Args:
            voice_id (str):
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            File
        """
        return (
            await self.with_raw_response.get_preview(
                voice_id=voice_id,
                talki_version=talki_version,
            )
        ).parse()

    async def list(
        self,
        *,
        talki_version: str | Unset = UNSET,
    ) -> VoiceList:
        """List voices

         Return every voice the assistant can speak with. The account's `voice` is one of these IDs. Requires
        `account:read`. Limited to 600 requests per minute per account (API key) or per installation
        (OAuth).

        Args:
            talki_version (str | Unset):  Example: 2026-10-01.

        Raises:
            talki.ApiError: The API answered with an error, as the subclass for its `type`.
            httpx.TimeoutException: If the request takes longer than the client's timeout.

        Returns:
            VoiceList
        """
        return (
            await self.with_raw_response.list(
                talki_version=talki_version,
            )
        ).parse()
