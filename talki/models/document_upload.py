from __future__ import annotations

from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="DocumentUpload")


@_attrs_define
class DocumentUpload:
    """A file, sent as `multipart/form-data`: PDF, DOCX, XLSX, TXT or CSV, at most 10 MB or the plan's lower limit.

    Attributes:
        file (File): The file: PDF, DOCX, XLSX, TXT or CSV, at most 10 MB or the account plan's lower limit. Its name
            becomes the document's `title`.
        location_ids (list[str] | None | Unset): Other locations that get a copy of it, ids from `GET /v1/locations`,
            one form field each.
    """

    file: File
    location_ids: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        location_ids: list[str] | None | Unset
        if isinstance(self.location_ids, Unset):
            location_ids = UNSET
        elif isinstance(self.location_ids, list):
            location_ids = self.location_ids

        else:
            location_ids = self.location_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
            }
        )
        if location_ids is not UNSET:
            field_dict["location_ids"] = location_ids

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("file", self.file.to_tuple()))

        if not isinstance(self.location_ids, Unset):
            if isinstance(self.location_ids, list):
                for location_ids_type_0_item_element in self.location_ids:
                    files.append(("location_ids", (None, str(location_ids_type_0_item_element).encode(), "text/plain")))
            else:
                files.append(("location_ids", (None, str(self.location_ids).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file = File(payload=BytesIO(d.pop("file")))

        def _parse_location_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                location_ids_type_0 = cast(list[str], data)

                return location_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        location_ids = _parse_location_ids(d.pop("location_ids", UNSET))

        document_upload = cls(
            file=file,
            location_ids=location_ids,
        )

        document_upload.additional_properties = d
        return document_upload

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
