from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DocumentText")


@_attrs_define
class DocumentText:
    """The text the assistant reads from a document: a note's text as written, or what Talki read from a file or a website,
    as the assistant searches it. Consecutive passages may repeat a few words where they overlap.

        Attributes:
            document_id (str): The document's identifier.
            text (str): A note's text as last written, even while it is `processing`. For a file or a website, the text read
                from it, as the assistant searches it: the passages in order, separated by a blank line, and empty until it is
                first `ready`.
    """

    document_id: str
    text: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        document_id = self.document_id

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "document_id": document_id,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        document_id = d.pop("document_id")

        text = d.pop("text")

        document_text = cls(
            document_id=document_id,
            text=text,
        )

        document_text.additional_properties = d
        return document_text

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
