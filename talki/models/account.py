from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.answers_as import AnswersAs

if TYPE_CHECKING:
    from ..models.account_languages import AccountLanguages
    from ..models.account_line import AccountLine
    from ..models.transfer_number import TransferNumber


T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """The account a credential belongs to, and everything its owner sets up for the assistant: the business name and
    texts, the voice, the opening and greeting, the switches, the transfer numbers, and the line that forwards to Talki.
    `GET /v1/account` needs only `account:read`, which makes it the call to validate a new credential. The settings are
    those of one location: the main one, or the one `?location_id=` names; the account's own switches read the same at
    every location. The response's `ETag` covers every writable field at that location; send it back as `If-Match` on
    `PATCH /v1/account` with the same `location_id`. `account.updated` reports a change to the main location's settings
    or to the account's switches, `location.settings_updated` one to another location's.

        Attributes:
            id (str): Opaque Talki account identifier.
            location_id (str): The location these settings are of, an id from `GET /v1/locations`: the one the request named
                with `location_id`, or the main location when it named none.
            business_name (None | str): The trading name the assistant uses for the business. Null if not yet configured.
            timezone (str): IANA timezone all naive local times for this account resolve against.
            livemode (bool): False when this credential does not act on real data: a test-mode key (`talki_test_…`), or an
                app installed on a developer sandbox or on a test account. Webhook envelopes carry the same flag.
            test (bool): True for a test account your app created with `"test": true` on `POST /oauth/managed-accounts`. It
                has no Talki number, nobody is billed for it or emailed, and it is erased seven days after it was created. Its
                `livemode` is false.
            business_information (None | str): Facts about the business that the assistant can tell callers, as the owner
                wrote them in Talki under «Informazioni aggiuntive», such as "parking is free" or "we do not deliver". Null when
                empty. This is not the assistant's full set of instructions: it sits inside Talki's own rules, which cannot be
                read or changed.
            instructions (None | str): Short orders about how the assistant should behave on a call, as the owner wrote them
                in Talki under «Istruzioni aggiuntive», such as "always use the formal lei" or "never quote prices on the
                phone". Null when empty. Like `business_information`, this sits inside Talki's own rules, which cannot be read
                or changed.
            voice (str): The voice the assistant speaks with on calls. One of the ids listed by `GET /v1/voices`.
            answers_as (AnswersAs): Which name the assistant answers calls in and speaks for: `business` uses the business
                name, `owner` the account holder's own name.
            greeting (None | str): What the assistant says right after its opening sentence, such as "Come posso aiutarla?".
                `{company_name}` and `{owner_name}` are replaced with the business name and the owner's name. Null when the
                assistant adds nothing after the opening.
            call_opening (None | str): The start of the first sentence a caller hears, such as "Buongiorno, sono Isa". Talki
                always completes it with a fixed statement that the caller is speaking to a virtual assistant, which cannot be
                changed. Null means the default opening, "Buongiorno, sta parlando con Talki". A custom opening is spoken only
                while the account's plan includes it; otherwise the default is used and this value is kept.
            multilingual_enabled (bool): True when the assistant may switch to English, French, German or Spanish to follow
                the caller. False keeps every call in Italian. The opening is always in Italian.
            languages (AccountLanguages): The languages the assistant speaks on calls, ISO 639-1. Read only: change them
                through `multilingual_enabled`.
            service_area (None | str): Where the business works or delivers, as free text the assistant can tell callers,
                such as "Bergamo e provincia". Null when not set.
            transfer_numbers (list[TransferNumber]): People or lines the assistant may hand a call over to. Empty when the
                assistant never transfers calls.
            bookings_enabled (bool): True when the assistant books, moves and cancels appointments on calls. False makes it
                answer questions and take messages only. Does not affect the appointment endpoints of this API.
            unresolved_requests_enabled (bool): True when the assistant offers to record a question it cannot answer, so the
                business can follow up. Recorded questions are listed by `GET /v1/unresolved_requests`.
            remember_callers (bool): True when the assistant recognises returning callers from the contact book and keeps
                notes about them for their next call. False treats every call as a first call and keeps nothing about the caller
                after it ends.
            notify_on_every_call (bool): True when the owner gets a push notification on the Talki mobile app after each
                call, with its summary. Push only, and only on phones where the owner is signed in to the app with notifications
                allowed; bookings, conflicts and unresolved questions push whatever this says. Talki sends no email or SMS per
                call: build those on the `call.ended` and `appointment.created` events.
            notify_on_incoming_call (bool): True when the owner gets a push notification on the Talki mobile app while a
                call is ringing, naming the caller, for every caller. Callers marked VIP push whatever this says. Push only, as
                for `notify_on_every_call`.
            store_transcripts (bool): True when the words of each call to this location are kept, readable through `GET
                /v1/calls/{id}/transcript`. Setting it to false deletes the transcripts already stored for this location's
                calls; call records and summaries are kept.
            phone_number (None | str): The Talki number that answers the location's calls, E.164. The business forwards the
                location's own line to it. Null until a number is assigned, and again once it is released; a location other than
                the main one has none while it is inactive. Read only; assigning or releasing it sends `account.updated` for the
                main location and `location.updated` for any other.
            forwarding_number (None | str): The location's own line, which forwards its calls to `phone_number`, E.164.
                `POST /v1/forwarding_check` rings it to prove forwarding is on. Null when not set.
            line (AccountLine): How calls reach Talki: the location's own line forwards to its Talki number. Read only. A
                check still ringing, or one that found no forwarding, is read from `GET /v1/forwarding_check`.
            multi_sede (bool): True when the account works from several locations, or may add them: show locations (`GET
                /v1/locations`) to the owner only when true. False for an account that has only ever had its main location and
                cannot add another; it still has that one location, every record still carries its `location_id`, and nothing
                changes shape when this turns true. Read only.
            onboarding_completed (bool): True once the account has finished setting up its assistant. While false, the Talki
                app opens its setup wizard. Set it with `POST /v1/account/complete_onboarding`; it never goes back to false.
    """

    id: str
    location_id: str
    business_name: None | str
    timezone: str
    livemode: bool
    test: bool
    business_information: None | str
    instructions: None | str
    voice: str
    answers_as: AnswersAs
    greeting: None | str
    call_opening: None | str
    multilingual_enabled: bool
    languages: AccountLanguages
    service_area: None | str
    transfer_numbers: list[TransferNumber]
    bookings_enabled: bool
    unresolved_requests_enabled: bool
    remember_callers: bool
    notify_on_every_call: bool
    notify_on_incoming_call: bool
    store_transcripts: bool
    phone_number: None | str
    forwarding_number: None | str
    line: AccountLine
    multi_sede: bool
    onboarding_completed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        location_id = self.location_id

        business_name: None | str
        business_name = self.business_name

        timezone = self.timezone

        livemode = self.livemode

        test = self.test

        business_information: None | str
        business_information = self.business_information

        instructions: None | str
        instructions = self.instructions

        voice = self.voice

        answers_as = self.answers_as.value

        greeting: None | str
        greeting = self.greeting

        call_opening: None | str
        call_opening = self.call_opening

        multilingual_enabled = self.multilingual_enabled

        languages = self.languages.to_dict()

        service_area: None | str
        service_area = self.service_area

        transfer_numbers = []
        for transfer_numbers_item_data in self.transfer_numbers:
            transfer_numbers_item = transfer_numbers_item_data.to_dict()
            transfer_numbers.append(transfer_numbers_item)

        bookings_enabled = self.bookings_enabled

        unresolved_requests_enabled = self.unresolved_requests_enabled

        remember_callers = self.remember_callers

        notify_on_every_call = self.notify_on_every_call

        notify_on_incoming_call = self.notify_on_incoming_call

        store_transcripts = self.store_transcripts

        phone_number: None | str
        phone_number = self.phone_number

        forwarding_number: None | str
        forwarding_number = self.forwarding_number

        line = self.line.to_dict()

        multi_sede = self.multi_sede

        onboarding_completed = self.onboarding_completed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "location_id": location_id,
                "business_name": business_name,
                "timezone": timezone,
                "livemode": livemode,
                "test": test,
                "business_information": business_information,
                "instructions": instructions,
                "voice": voice,
                "answers_as": answers_as,
                "greeting": greeting,
                "call_opening": call_opening,
                "multilingual_enabled": multilingual_enabled,
                "languages": languages,
                "service_area": service_area,
                "transfer_numbers": transfer_numbers,
                "bookings_enabled": bookings_enabled,
                "unresolved_requests_enabled": unresolved_requests_enabled,
                "remember_callers": remember_callers,
                "notify_on_every_call": notify_on_every_call,
                "notify_on_incoming_call": notify_on_incoming_call,
                "store_transcripts": store_transcripts,
                "phone_number": phone_number,
                "forwarding_number": forwarding_number,
                "line": line,
                "multi_sede": multi_sede,
                "onboarding_completed": onboarding_completed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_languages import AccountLanguages  # noqa: PLC0415
        from ..models.account_line import AccountLine  # noqa: PLC0415
        from ..models.transfer_number import TransferNumber  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        location_id = d.pop("location_id")

        def _parse_business_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        business_name = _parse_business_name(d.pop("business_name"))

        timezone = d.pop("timezone")

        livemode = d.pop("livemode")

        test = d.pop("test")

        def _parse_business_information(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        business_information = _parse_business_information(d.pop("business_information"))

        def _parse_instructions(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        instructions = _parse_instructions(d.pop("instructions"))

        voice = d.pop("voice")

        answers_as = AnswersAs(d.pop("answers_as"))

        def _parse_greeting(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        greeting = _parse_greeting(d.pop("greeting"))

        def _parse_call_opening(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        call_opening = _parse_call_opening(d.pop("call_opening"))

        multilingual_enabled = d.pop("multilingual_enabled")

        languages = AccountLanguages.from_dict(d.pop("languages"))

        def _parse_service_area(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        service_area = _parse_service_area(d.pop("service_area"))

        transfer_numbers = []
        _transfer_numbers = d.pop("transfer_numbers")
        for transfer_numbers_item_data in _transfer_numbers:
            transfer_numbers_item = TransferNumber.from_dict(transfer_numbers_item_data)

            transfer_numbers.append(transfer_numbers_item)

        bookings_enabled = d.pop("bookings_enabled")

        unresolved_requests_enabled = d.pop("unresolved_requests_enabled")

        remember_callers = d.pop("remember_callers")

        notify_on_every_call = d.pop("notify_on_every_call")

        notify_on_incoming_call = d.pop("notify_on_incoming_call")

        store_transcripts = d.pop("store_transcripts")

        def _parse_phone_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone_number = _parse_phone_number(d.pop("phone_number"))

        def _parse_forwarding_number(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        forwarding_number = _parse_forwarding_number(d.pop("forwarding_number"))

        line = AccountLine.from_dict(d.pop("line"))

        multi_sede = d.pop("multi_sede")

        onboarding_completed = d.pop("onboarding_completed")

        account = cls(
            id=id,
            location_id=location_id,
            business_name=business_name,
            timezone=timezone,
            livemode=livemode,
            test=test,
            business_information=business_information,
            instructions=instructions,
            voice=voice,
            answers_as=answers_as,
            greeting=greeting,
            call_opening=call_opening,
            multilingual_enabled=multilingual_enabled,
            languages=languages,
            service_area=service_area,
            transfer_numbers=transfer_numbers,
            bookings_enabled=bookings_enabled,
            unresolved_requests_enabled=unresolved_requests_enabled,
            remember_callers=remember_callers,
            notify_on_every_call=notify_on_every_call,
            notify_on_incoming_call=notify_on_incoming_call,
            store_transcripts=store_transcripts,
            phone_number=phone_number,
            forwarding_number=forwarding_number,
            line=line,
            multi_sede=multi_sede,
            onboarding_completed=onboarding_completed,
        )

        account.additional_properties = d
        return account

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
