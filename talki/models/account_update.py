from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.answers_as import AnswersAs
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transfer_number_input import TransferNumberInput

from collections.abc import Sequence
from typing import Literal, TypedDict

if TYPE_CHECKING:
    from ..models.transfer_number_input import TransferNumberInputDict


T = TypeVar("T", bound="AccountUpdate")


@_attrs_define
class AccountUpdate:
    """The settings you can change. Every field is optional and an omitted one is left unchanged, but send at least one. A
    `null` or empty text clears it; a voice, a switch or the transfer list cannot be null. With `?location_id=`, a
    location's own settings change at that location only, and the account's switches at every location.

        Attributes:
            business_name (None | str | Unset): Replaces the business name. Send `null` or an empty string to clear it.
            business_information (None | str | Unset): Replaces the business information. Send `null` or an empty string to
                clear it.
            instructions (None | str | Unset): Replaces the instructions. Send `null` or an empty string to clear them. Keep
                them to a few short orders: longer text makes each one less likely to be followed.
            voice (None | str | Unset): A voice id from `GET /v1/voices`. Cannot be null.
            answers_as (AnswersAs | None | Unset): `business` or `owner`. Cannot be null.
            greeting (None | str | Unset): Replaces the greeting. May contain `{company_name}` and `{owner_name}`. Leading
                and trailing whitespace is removed. Send `null` or an empty string to clear it.
            call_opening (None | str | Unset): Replaces the opening, at most 160 characters once runs of whitespace are
                collapsed to one space. May contain `{company_name}` and `{owner_name}`. Setting one needs a plan that includes
                a custom opening, or the request is refused with `plan_feature_unavailable`. Send `null` or an empty string to
                go back to the default, which every plan may do.
            multilingual_enabled (bool | None | Unset): Cannot be null.
            service_area (None | str | Unset): Replaces the service area. Send `null` or an empty string to clear it.
            transfer_numbers (list[TransferNumberInput] | None | Unset): The whole list, replacing every existing entry.
                Send an empty list to remove them all; `null` is refused. A non-empty list needs the main location's
                `forwarding_number`, already stored or sent in the same request, and may not contain it, nor the location's own
                `forwarding_number`: a call transferred there would come straight back to the assistant.
            bookings_enabled (bool | None | Unset): Cannot be null.
            unresolved_requests_enabled (bool | None | Unset): Cannot be null.
            remember_callers (bool | None | Unset): Cannot be null.
            notify_on_every_call (bool | None | Unset): Cannot be null.
            notify_on_incoming_call (bool | None | Unset): Cannot be null.
            store_transcripts (bool | None | Unset): Cannot be null. `false` deletes the stored transcripts of this
                location's calls in the same request, and they cannot be recovered, so a test-mode credential sending it is
                refused with `livemode_required`.
            forwarding_number (None | str | Unset): Replaces the location's forwarding number: a mobile or landline that can
                be rung, E.164 or national (read as Italian). Send `null` or an empty string to clear it. Refused if it equals a
                transfer target of any location, or the line of another location, unless the same request replaces this
                location's `transfer_numbers`. The main location's cannot be cleared while any location has `transfer_numbers`.
                A change discards the result of the last forwarding check, and `last_verified_at` reads null until a check of
                the new number succeeds.
    """

    business_name: None | str | Unset = UNSET
    business_information: None | str | Unset = UNSET
    instructions: None | str | Unset = UNSET
    voice: None | str | Unset = UNSET
    answers_as: AnswersAs | None | Unset = UNSET
    greeting: None | str | Unset = UNSET
    call_opening: None | str | Unset = UNSET
    multilingual_enabled: bool | None | Unset = UNSET
    service_area: None | str | Unset = UNSET
    transfer_numbers: list[TransferNumberInput] | None | Unset = UNSET
    bookings_enabled: bool | None | Unset = UNSET
    unresolved_requests_enabled: bool | None | Unset = UNSET
    remember_callers: bool | None | Unset = UNSET
    notify_on_every_call: bool | None | Unset = UNSET
    notify_on_incoming_call: bool | None | Unset = UNSET
    store_transcripts: bool | None | Unset = UNSET
    forwarding_number: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        business_name: None | str | Unset
        if isinstance(self.business_name, Unset):
            business_name = UNSET
        else:
            business_name = self.business_name

        business_information: None | str | Unset
        if isinstance(self.business_information, Unset):
            business_information = UNSET
        else:
            business_information = self.business_information

        instructions: None | str | Unset
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        voice: None | str | Unset
        if isinstance(self.voice, Unset):
            voice = UNSET
        else:
            voice = self.voice

        answers_as: None | str | Unset
        if isinstance(self.answers_as, Unset):
            answers_as = UNSET
        elif isinstance(self.answers_as, AnswersAs):
            answers_as = self.answers_as.value
        else:
            answers_as = self.answers_as

        greeting: None | str | Unset
        if isinstance(self.greeting, Unset):
            greeting = UNSET
        else:
            greeting = self.greeting

        call_opening: None | str | Unset
        if isinstance(self.call_opening, Unset):
            call_opening = UNSET
        else:
            call_opening = self.call_opening

        multilingual_enabled: bool | None | Unset
        if isinstance(self.multilingual_enabled, Unset):
            multilingual_enabled = UNSET
        else:
            multilingual_enabled = self.multilingual_enabled

        service_area: None | str | Unset
        if isinstance(self.service_area, Unset):
            service_area = UNSET
        else:
            service_area = self.service_area

        transfer_numbers: list[dict[str, Any]] | None | Unset
        if isinstance(self.transfer_numbers, Unset):
            transfer_numbers = UNSET
        elif isinstance(self.transfer_numbers, list):
            transfer_numbers = []
            for transfer_numbers_type_0_item_data in self.transfer_numbers:
                transfer_numbers_type_0_item = transfer_numbers_type_0_item_data.to_dict()
                transfer_numbers.append(transfer_numbers_type_0_item)

        else:
            transfer_numbers = self.transfer_numbers

        bookings_enabled: bool | None | Unset
        if isinstance(self.bookings_enabled, Unset):
            bookings_enabled = UNSET
        else:
            bookings_enabled = self.bookings_enabled

        unresolved_requests_enabled: bool | None | Unset
        if isinstance(self.unresolved_requests_enabled, Unset):
            unresolved_requests_enabled = UNSET
        else:
            unresolved_requests_enabled = self.unresolved_requests_enabled

        remember_callers: bool | None | Unset
        if isinstance(self.remember_callers, Unset):
            remember_callers = UNSET
        else:
            remember_callers = self.remember_callers

        notify_on_every_call: bool | None | Unset
        if isinstance(self.notify_on_every_call, Unset):
            notify_on_every_call = UNSET
        else:
            notify_on_every_call = self.notify_on_every_call

        notify_on_incoming_call: bool | None | Unset
        if isinstance(self.notify_on_incoming_call, Unset):
            notify_on_incoming_call = UNSET
        else:
            notify_on_incoming_call = self.notify_on_incoming_call

        store_transcripts: bool | None | Unset
        if isinstance(self.store_transcripts, Unset):
            store_transcripts = UNSET
        else:
            store_transcripts = self.store_transcripts

        forwarding_number: None | str | Unset
        if isinstance(self.forwarding_number, Unset):
            forwarding_number = UNSET
        else:
            forwarding_number = self.forwarding_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if business_name is not UNSET:
            field_dict["business_name"] = business_name
        if business_information is not UNSET:
            field_dict["business_information"] = business_information
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if voice is not UNSET:
            field_dict["voice"] = voice
        if answers_as is not UNSET:
            field_dict["answers_as"] = answers_as
        if greeting is not UNSET:
            field_dict["greeting"] = greeting
        if call_opening is not UNSET:
            field_dict["call_opening"] = call_opening
        if multilingual_enabled is not UNSET:
            field_dict["multilingual_enabled"] = multilingual_enabled
        if service_area is not UNSET:
            field_dict["service_area"] = service_area
        if transfer_numbers is not UNSET:
            field_dict["transfer_numbers"] = transfer_numbers
        if bookings_enabled is not UNSET:
            field_dict["bookings_enabled"] = bookings_enabled
        if unresolved_requests_enabled is not UNSET:
            field_dict["unresolved_requests_enabled"] = unresolved_requests_enabled
        if remember_callers is not UNSET:
            field_dict["remember_callers"] = remember_callers
        if notify_on_every_call is not UNSET:
            field_dict["notify_on_every_call"] = notify_on_every_call
        if notify_on_incoming_call is not UNSET:
            field_dict["notify_on_incoming_call"] = notify_on_incoming_call
        if store_transcripts is not UNSET:
            field_dict["store_transcripts"] = store_transcripts
        if forwarding_number is not UNSET:
            field_dict["forwarding_number"] = forwarding_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transfer_number_input import TransferNumberInput  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_business_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        business_name = _parse_business_name(d.pop("business_name", UNSET))

        def _parse_business_information(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        business_information = _parse_business_information(d.pop("business_information", UNSET))

        def _parse_instructions(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        def _parse_voice(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        voice = _parse_voice(d.pop("voice", UNSET))

        def _parse_answers_as(data: object) -> AnswersAs | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                answers_as_type_0 = AnswersAs(data)

                return answers_as_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AnswersAs | None | Unset, data)

        answers_as = _parse_answers_as(d.pop("answers_as", UNSET))

        def _parse_greeting(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        greeting = _parse_greeting(d.pop("greeting", UNSET))

        def _parse_call_opening(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        call_opening = _parse_call_opening(d.pop("call_opening", UNSET))

        def _parse_multilingual_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        multilingual_enabled = _parse_multilingual_enabled(d.pop("multilingual_enabled", UNSET))

        def _parse_service_area(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service_area = _parse_service_area(d.pop("service_area", UNSET))

        def _parse_transfer_numbers(data: object) -> list[TransferNumberInput] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                transfer_numbers_type_0 = []
                _transfer_numbers_type_0 = data
                for transfer_numbers_type_0_item_data in _transfer_numbers_type_0:
                    transfer_numbers_type_0_item = TransferNumberInput.from_dict(transfer_numbers_type_0_item_data)

                    transfer_numbers_type_0.append(transfer_numbers_type_0_item)

                return transfer_numbers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[TransferNumberInput] | None | Unset, data)

        transfer_numbers = _parse_transfer_numbers(d.pop("transfer_numbers", UNSET))

        def _parse_bookings_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        bookings_enabled = _parse_bookings_enabled(d.pop("bookings_enabled", UNSET))

        def _parse_unresolved_requests_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        unresolved_requests_enabled = _parse_unresolved_requests_enabled(d.pop("unresolved_requests_enabled", UNSET))

        def _parse_remember_callers(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        remember_callers = _parse_remember_callers(d.pop("remember_callers", UNSET))

        def _parse_notify_on_every_call(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        notify_on_every_call = _parse_notify_on_every_call(d.pop("notify_on_every_call", UNSET))

        def _parse_notify_on_incoming_call(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        notify_on_incoming_call = _parse_notify_on_incoming_call(d.pop("notify_on_incoming_call", UNSET))

        def _parse_store_transcripts(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        store_transcripts = _parse_store_transcripts(d.pop("store_transcripts", UNSET))

        def _parse_forwarding_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        forwarding_number = _parse_forwarding_number(d.pop("forwarding_number", UNSET))

        account_update = cls(
            business_name=business_name,
            business_information=business_information,
            instructions=instructions,
            voice=voice,
            answers_as=answers_as,
            greeting=greeting,
            call_opening=call_opening,
            multilingual_enabled=multilingual_enabled,
            service_area=service_area,
            transfer_numbers=transfer_numbers,
            bookings_enabled=bookings_enabled,
            unresolved_requests_enabled=unresolved_requests_enabled,
            remember_callers=remember_callers,
            notify_on_every_call=notify_on_every_call,
            notify_on_incoming_call=notify_on_incoming_call,
            store_transcripts=store_transcripts,
            forwarding_number=forwarding_number,
        )

        account_update.additional_properties = d
        return account_update

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


# `AccountUpdate` as a dict, which a method's `body=` takes in its place: a key
# left out is a field left out. A date, datetime or UUID can be its ISO string,
# an enum its value.
class AccountUpdateDict(TypedDict, total=False):
    business_name: str | None
    business_information: str | None
    instructions: str | None
    voice: str | None
    answers_as: AnswersAs | Literal["business", "owner"] | None
    greeting: str | None
    call_opening: str | None
    multilingual_enabled: bool | None
    service_area: str | None
    transfer_numbers: Sequence[TransferNumberInputDict | TransferNumberInput] | None
    bookings_enabled: bool | None
    unresolved_requests_enabled: bool | None
    remember_callers: bool | None
    notify_on_every_call: bool | None
    notify_on_incoming_call: bool | None
    store_transcripts: bool | None
    forwarding_number: str | None
