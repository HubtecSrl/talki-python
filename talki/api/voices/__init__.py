"""The `voices` operations, one module each, and `VoicesResource` / `AsyncVoicesResource`,
which `Talki` and `AsyncTalki` expose as `voices`."""

from ... import _resource
from ...models.voice_list import VoiceList
from ...types import UNSET, File, Unset
from . import (
    get_voice_preview,
    list_voices,
)

__all__ = ["AsyncVoicesResource", "VoicesResource"]


class VoicesResource(_resource.Resource):
    """`talki.voices`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

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
        return _resource.unwrap(
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
        return _resource.unwrap(
            list_voices.sync_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )


class AsyncVoicesResource(_resource.Resource):
    """`talki.voices` on `AsyncTalki`: each method sends one operation and returns its value, or
    raises the `talki.ApiError` subclass for its error."""

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
        return _resource.unwrap(
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
        return _resource.unwrap(
            await list_voices.asyncio_detailed(
                client=self._client,
                talki_version=talki_version,
            )
        )
