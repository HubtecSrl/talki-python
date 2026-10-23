from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.transcript_utterance_speaker import TranscriptUtteranceSpeaker

T = TypeVar("T", bound="TranscriptUtterance")


@_attrs_define
class TranscriptUtterance:
    """One turn of the conversation. Skip or mark a turn whose `unreliable` is true: its `text` is a placeholder. An
    `omitted` turn marks where the middle of a long call was left out.

        Attributes:
            speaker (TranscriptUtteranceSpeaker): Who spoke. `omitted` is not speech: it marks where the middle of an
                unusually long call was left out, and its `text` says how many turns. The start and the end of the call are
                always kept.
            text (str): What was said, as transcribed automatically during the call. It can be wrong: background speech may
                be captured as the caller's, and a turn may come out in the wrong language. Not a verbatim record.
            offset_ms (int | None): Milliseconds from the first turn of the call to the start of this one. Null when it was
                not measured, and on an `omitted` marker.
            duration_ms (int | None): How long the turn lasted, in milliseconds. Null when not measured.
            interrupted (bool): True when the caller spoke over the assistant and it stopped: the caller heard only the
                beginning of `text`. Always false for the caller.
            unreliable (bool): True when the transcription of this turn was judged to be noise. `text` is then a
                placeholder, not something anyone said.
            retranscribed (bool): True when this turn was transcribed again from the call audio after the call, and that
                transcription replaced the one made during the call.
    """

    speaker: TranscriptUtteranceSpeaker
    text: str
    offset_ms: int | None
    duration_ms: int | None
    interrupted: bool
    unreliable: bool
    retranscribed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        speaker = self.speaker.value

        text = self.text

        offset_ms: int | None
        offset_ms = self.offset_ms

        duration_ms: int | None
        duration_ms = self.duration_ms

        interrupted = self.interrupted

        unreliable = self.unreliable

        retranscribed = self.retranscribed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "speaker": speaker,
                "text": text,
                "offset_ms": offset_ms,
                "duration_ms": duration_ms,
                "interrupted": interrupted,
                "unreliable": unreliable,
                "retranscribed": retranscribed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        speaker = TranscriptUtteranceSpeaker(d.pop("speaker"))

        text = d.pop("text")

        def _parse_offset_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        offset_ms = _parse_offset_ms(d.pop("offset_ms"))

        def _parse_duration_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        duration_ms = _parse_duration_ms(d.pop("duration_ms"))

        interrupted = d.pop("interrupted")

        unreliable = d.pop("unreliable")

        retranscribed = d.pop("retranscribed")

        transcript_utterance = cls(
            speaker=speaker,
            text=text,
            offset_ms=offset_ms,
            duration_ms=duration_ms,
            interrupted=interrupted,
            unreliable=unreliable,
            retranscribed=retranscribed,
        )

        transcript_utterance.additional_properties = d
        return transcript_utterance

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
