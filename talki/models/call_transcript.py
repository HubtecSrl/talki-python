from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.transcript_utterance import TranscriptUtterance


T = TypeVar("T", bound="CallTranscript")


@_attrs_define
class CallTranscript:
    """The automatic transcript of one call. The text is machine-made and can be wrong, so show it as an automatic
    transcript, never as a verbatim record. It is deleted with its call, and when the account stops keeping transcripts;
    from then on this endpoint answers `transcript_not_available`.

        Attributes:
            call_id (str): The call this transcript belongs to.
            utterances (list[TranscriptUtterance]): The turns, in the order they were spoken.
            source (str): Which transcription pipeline produced the text. Today always `gemini_live_sidechannel`:
                transcribed live, during the call. Treat an unknown value as another automatic pipeline.
            language_hint (None | str): The language transcription was told to expect. `auto` means it followed the caller,
                who may switch language mid-call.
            assembler (int): Version of the code that cut the audio into turns. Rises when that changes, so two transcripts
                made differently can be told apart.
            created_at (datetime.datetime): When Talki stored this transcript, just after the call ended. RFC 3339 UTC.
    """

    call_id: str
    utterances: list[TranscriptUtterance]
    source: str
    language_hint: None | str
    assembler: int
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call_id = self.call_id

        utterances = []
        for utterances_item_data in self.utterances:
            utterances_item = utterances_item_data.to_dict()
            utterances.append(utterances_item)

        source = self.source

        language_hint: None | str
        language_hint = self.language_hint

        assembler = self.assembler

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call_id": call_id,
                "utterances": utterances,
                "source": source,
                "language_hint": language_hint,
                "assembler": assembler,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transcript_utterance import TranscriptUtterance  # noqa: PLC0415

        d = dict(src_dict)
        call_id = d.pop("call_id")

        utterances = []
        _utterances = d.pop("utterances")
        for utterances_item_data in _utterances:
            utterances_item = TranscriptUtterance.from_dict(utterances_item_data)

            utterances.append(utterances_item)

        source = d.pop("source")

        def _parse_language_hint(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        language_hint = _parse_language_hint(d.pop("language_hint"))

        assembler = d.pop("assembler")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        call_transcript = cls(
            call_id=call_id,
            utterances=utterances,
            source=source,
            language_hint=language_hint,
            assembler=assembler,
            created_at=created_at,
        )

        call_transcript.additional_properties = d
        return call_transcript

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
