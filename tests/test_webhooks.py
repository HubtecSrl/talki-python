"""`talki.webhooks` against signatures made as Talki makes them:
`t=<unix seconds>`, then one `v1=<hex HMAC-SHA256 of "<t>.<body>">` per
secret, the previous secret's first while a rotation overlaps."""

import hashlib
import hmac
import json

import pytest

from talki.webhooks import (
    SIGNATURE_HEADER,
    SignatureVerificationError,
    construct_event,
    signature_of,
    verify_signature,
)

NOW = 1_790_000_000
EVENT = {"id": "evt_1", "type": "call.ended", "livemode": False, "data": {"object": {"caller": "Niccolò Bianchi"}}}
# As the server writes it: compact, UTF-8, non-ASCII kept.
BODY = json.dumps(EVENT, separators=(",", ":"), ensure_ascii=False).encode()


def _v1(secret: str, at: int, body: bytes) -> str:
    return hmac.new(secret.encode(), f"{at}.".encode() + body, hashlib.sha256).hexdigest()


def signed(body: bytes, secret: str, previous: str | None = None, at: int = NOW) -> str:
    parts = [f"t={at}"]
    if previous:
        parts.append(f"v1={_v1(previous, at, body)}")
    parts.append(f"v1={_v1(secret, at, body)}")
    return ",".join(parts)


def test_a_known_signature_verifies():
    # Fixed bytes, fixed secret, fixed time: a vector that pins the format
    # independently of the signer above.
    header = "t=1790000000,v1=" + hmac.new(b"whsec_vector", b"1790000000.{}", hashlib.sha256).hexdigest()
    verify_signature(b"{}", header, "whsec_vector", now=NOW)


def test_the_header_is_found_whatever_its_case():
    header = signed(BODY, "whsec_current")
    for headers in ({SIGNATURE_HEADER: header}, {SIGNATURE_HEADER.lower(): header}):
        assert construct_event(BODY, signature_of(headers), "whsec_current", now=NOW) == EVENT
    assert signature_of({"Content-Type": "application/json"}) is None


def test_a_delivery_the_server_signed_verifies():
    header = signed(BODY, "whsec_current")
    verify_signature(BODY, header, "whsec_current", now=NOW + 10)
    assert construct_event(BODY, header, "whsec_current", now=NOW) == EVENT


def test_both_secrets_verify_during_a_rotation():
    header = signed(BODY, "whsec_new", previous="whsec_old")
    verify_signature(BODY, header, "whsec_new", now=NOW)
    verify_signature(BODY, header, "whsec_old", now=NOW)
    verify_signature(BODY, header, ["whsec_unrelated", "whsec_new"], now=NOW)


@pytest.mark.parametrize(
    ("body", "header", "secret", "now"),
    [
        (BODY, None, "whsec_current", NOW),
        (BODY, "garbage", "whsec_current", NOW),
        (BODY, "t=abc,v1=00", "whsec_current", NOW),
        (BODY, signed(BODY, "whsec_current"), "whsec_other", NOW),
        # Re-serialised with ASCII escapes: other bytes, so another signature.
        (json.dumps(EVENT).encode(), signed(BODY, "whsec_current"), "whsec_current", NOW),
        (BODY, signed(BODY, "whsec_current"), "whsec_current", NOW + 301),
        (BODY, signed(BODY, "whsec_current"), "whsec_current", NOW - 301),
    ],
    ids=["no-header", "malformed", "bad-timestamp", "wrong-secret", "reserialised-body", "too-old", "from-the-future"],
)
def test_what_is_refused(body, header, secret, now):
    with pytest.raises(SignatureVerificationError):
        verify_signature(body, header, secret, now=now)


def test_a_missing_secret_is_a_programming_error():
    with pytest.raises(ValueError):
        verify_signature(BODY, signed(BODY, "whsec_current"), "", now=NOW)


def test_a_signed_body_that_is_not_an_event_is_refused():
    body = b"[1, 2]"
    with pytest.raises(SignatureVerificationError):
        construct_event(body, signed(body, "whsec_current"), "whsec_current", now=NOW)


GOOD = signed(BODY, "whsec_current")
V1 = GOOD.split("v1=")[1]


@pytest.mark.parametrize(
    "header",
    [
        f"t={NOW},v1=é",  # latin-1 bytes a framework decoded: no match, never a crash
        f"t={NOW},v1=",
        f"T={NOW},V1={V1}",
        f"{GOOD},t={NOW + 1}",  # a second t: the last one is the one checked
        f"t={'9' * 400},v1={V1}",
    ],
    ids=["non-ascii", "empty-v1", "uppercase-names", "injected-t", "huge-t"],
)
def test_odd_headers_are_refused_cleanly(header):
    with pytest.raises(SignatureVerificationError):
        verify_signature(BODY, header, "whsec_current", now=NOW)


def test_tolerated_header_shapes():
    verify_signature(BODY, f" t={NOW} , v1=nothex , v1={V1} ", "whsec_current", now=NOW)
    verify_signature(BODY, f"t={NOW},v1=,v1={V1}", "whsec_current", now=NOW)
    verify_signature(BODY, GOOD.encode(), b"whsec_current", now=NOW + 300)
    verify_signature(BODY, signed(BODY, "whsec_new", previous="whsec_old"), ["whsec_old", "whsec_new"], now=NOW)


def test_a_decoded_body_is_a_programming_error():
    with pytest.raises(TypeError):
        verify_signature(BODY.decode(), GOOD, "whsec_current", now=NOW)


def test_a_signed_body_that_is_not_json_is_refused():
    body = b"not json"
    with pytest.raises(SignatureVerificationError):
        construct_event(body, signed(body, "whsec_current"), "whsec_current", now=NOW)


def test_a_bytes_secret_is_the_key_as_given():
    key = "whsec_é"
    verify_signature(BODY, signed(BODY, key), key.encode(), now=NOW)
    verify_signature(BODY, signed(BODY, key), key, now=NOW)
