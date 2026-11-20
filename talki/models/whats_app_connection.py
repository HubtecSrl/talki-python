from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WhatsAppConnection")


@_attrs_define
class WhatsAppConnection:
    """The connected WhatsApp Business number.

    Attributes:
        state (str): `not_connected` (never connected), `connected`, or `disconnected` (connected once, removed since).
            The owner connects the number in the Talki app; the API cannot.
        phone_number (None | str): The number, E.164: the connected one, or the last one connected once `disconnected`.
            Null when never connected.
        business_name (None | str): The business's name as WhatsApp shows it to customers, or null.
        connected_at (datetime.datetime | None): When it was connected, RFC 3339 UTC, or null.
        disconnected_at (datetime.datetime | None): When it was removed, RFC 3339 UTC, or null while connected.
        quality_rating (None | str): WhatsApp's quality rating of the number: `GREEN`, `YELLOW`, `RED` or `UNKNOWN`, or
            null when WhatsApp has not given one.
        restricted (bool): True while WhatsApp restricts the number: Talki sends nothing.
        payment_method (bool | None): Whether the WhatsApp account has a payment method: `false` once WhatsApp refused a
            message for lack of one, and then Talki sends nothing; `true` once a message went through. Null until the first
            message settles it, as for a number just connected: Talki sends.
    """

    state: str
    phone_number: None | str
    business_name: None | str
    connected_at: datetime.datetime | None
    disconnected_at: datetime.datetime | None
    quality_rating: None | str
    restricted: bool
    payment_method: bool | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state

        phone_number: None | str
        phone_number = self.phone_number

        business_name: None | str
        business_name = self.business_name

        connected_at: None | str
        if isinstance(self.connected_at, datetime.datetime):
            connected_at = self.connected_at.isoformat()
        else:
            connected_at = self.connected_at

        disconnected_at: None | str
        if isinstance(self.disconnected_at, datetime.datetime):
            disconnected_at = self.disconnected_at.isoformat()
        else:
            disconnected_at = self.disconnected_at

        quality_rating: None | str
        quality_rating = self.quality_rating

        restricted = self.restricted

        payment_method: bool | None
        payment_method = self.payment_method

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "phone_number": phone_number,
                "business_name": business_name,
                "connected_at": connected_at,
                "disconnected_at": disconnected_at,
                "quality_rating": quality_rating,
                "restricted": restricted,
                "payment_method": payment_method,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = d.pop("state")

        def _parse_phone_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_number = _parse_phone_number(d.pop("phone_number"))

        def _parse_business_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        business_name = _parse_business_name(d.pop("business_name"))

        def _parse_connected_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                connected_at_type_0 = datetime.datetime.fromisoformat(data)

                return connected_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        connected_at = _parse_connected_at(d.pop("connected_at"))

        def _parse_disconnected_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                disconnected_at_type_0 = datetime.datetime.fromisoformat(data)

                return disconnected_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        disconnected_at = _parse_disconnected_at(d.pop("disconnected_at"))

        def _parse_quality_rating(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        quality_rating = _parse_quality_rating(d.pop("quality_rating"))

        restricted = d.pop("restricted")

        def _parse_payment_method(data: object) -> bool | None:
            if data is None:
                return data
            return cast(bool | None, data)

        payment_method = _parse_payment_method(d.pop("payment_method"))

        whats_app_connection = cls(
            state=state,
            phone_number=phone_number,
            business_name=business_name,
            connected_at=connected_at,
            disconnected_at=disconnected_at,
            quality_rating=quality_rating,
            restricted=restricted,
            payment_method=payment_method,
        )

        whats_app_connection.additional_properties = d
        return whats_app_connection

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
