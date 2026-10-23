"""The generated part of `talki` read against answers it
was not generated for: a value added to a response enum must parse."""

from enum import StrEnum

import httpx
import pytest

import talki.models
from talki import AuthenticatedClient
from talki.api.account import get_account
from talki.models import ErrorDetailType, ErrorEnvelope

GENERATED_ENUMS = sorted(
    (value for value in vars(talki.models).values() if isinstance(value, type) and issubclass(value, StrEnum)),
    key=lambda enum: enum.__name__,
)


def test_the_sdk_has_enums_to_check():
    assert ErrorDetailType in GENERATED_ENUMS


@pytest.mark.parametrize("enum", GENERATED_ENUMS, ids=lambda enum: enum.__name__)
def test_every_enum_reads_a_value_it_does_not_list(enum):
    added = enum("value_added_later")

    assert isinstance(added, enum)
    assert added == "value_added_later"
    assert str(added) == "value_added_later"
    assert added.value == "value_added_later"
    assert added not in list(enum)
    # Parsed again, it is the same member, as a listed value would be.
    assert enum("value_added_later") is added
    # The listed members are untouched.
    for member in enum:
        assert enum(member.value) is member


@pytest.mark.parametrize("enum", GENERATED_ENUMS, ids=lambda enum: enum.__name__)
def test_an_enum_still_refuses_what_is_not_a_string(enum):
    with pytest.raises(ValueError):
        enum(3)


def test_an_error_envelope_with_a_new_type_parses():
    body = {
        "error": {
            "type": "brand_new_type",
            "code": "brand_new_code",
            "message": "Something the client predates.",
            "request_id": "req_0123",
        }
    }

    def answer(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json=body)

    client = AuthenticatedClient(
        base_url="https://api.example.test",
        token="talki_test_x",
        httpx_args={"transport": httpx.MockTransport(answer)},
    )
    with client:
        parsed = get_account.sync(client=client)

    assert isinstance(parsed, ErrorEnvelope)
    assert parsed.error.type_ == "brand_new_type"
    assert parsed.error.code == "brand_new_code"
    assert parsed.to_dict() == body


def test_a_nullable_enum_field_reads_a_new_value_as_the_enum():
    from talki.models import AccountUpdate, AnswersAs

    update = AccountUpdate.from_dict({"answers_as": "value_added_later"})

    assert isinstance(update.answers_as, AnswersAs)
    assert update.answers_as == "value_added_later"
    assert update.to_dict() == {"answers_as": "value_added_later"}
