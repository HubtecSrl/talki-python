from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.voice_gender import VoiceGender

T = TypeVar("T", bound="Voice")


@_attrs_define
class Voice:
    """One voice the assistant can speak with on calls. Set it as `voice` with `PATCH /v1/account`.

    Attributes:
        id (str): Voice id, the value `voice` takes on the account.
        name (str): Display name of the voice.
        gender (VoiceGender): Whether the voice sounds female or male.
        preview_url (str): Path of a short WAV sample of this voice, relative to the API base URL. Fetch it with the
            same credential.
    """

    id: str
    name: str
    gender: VoiceGender
    preview_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        gender = self.gender.value

        preview_url = self.preview_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "gender": gender,
                "preview_url": preview_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        gender = VoiceGender(d.pop("gender"))

        preview_url = d.pop("preview_url")

        voice = cls(
            id=id,
            name=name,
            gender=gender,
            preview_url=preview_url,
        )

        voice.additional_properties = d
        return voice

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
