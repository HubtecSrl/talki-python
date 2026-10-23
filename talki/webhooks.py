"""Check that a webhook or app event came from Talki, before trusting it.

    from talki.webhooks import SignatureVerificationError, construct_event, signature_of

    def receive(request):                                # your web framework's
        try:
            event = construct_event(request.body, signature_of(request.headers), secret)
        except SignatureVerificationError:
            return 400
        handle(event["type"], event["data"])
        return 200

Pass the body as the bytes received, before any JSON parsing: the signature is
over those exact bytes, and a re-serialised body differs as soon as it holds a
non-ASCII character. While a secret is rotated with an overlap the header
signs with both, so either one verifies; pass a list when you hold more than
one.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from collections.abc import Mapping, Sequence
from typing import Any

from .exceptions import TalkiError

__all__ = [
    "DELIVERY_HEADER",
    "EVENT_HEADER",
    "SIGNATURE_HEADER",
    "TOLERANCE_SECONDS",
    "SignatureVerificationError",
    "construct_event",
    "signature_of",
    "verify_signature",
]

SIGNATURE_HEADER = "X-Talki-Signature"
EVENT_HEADER = "X-Talki-Event"
DELIVERY_HEADER = "X-Talki-Delivery"
# How far a signed timestamp may be from now before the delivery is refused as
# a possible replay.
TOLERANCE_SECONDS = 300


class SignatureVerificationError(TalkiError):
    """The delivery is not provably from Talki: answer it 400 and ignore it."""


_HEX_DIGEST_LENGTH = 64
_HEX = frozenset("0123456789abcdef")


def signature_of(headers: Mapping[str, str]) -> str | None:
    """`X-Talki-Signature` from a request's headers, whatever their case (a
    plain dict from a gateway may hold them lowercased)."""
    wanted = SIGNATURE_HEADER.lower()
    return next((value for key, value in headers.items() if key.lower() == wanted), None)


def _text(value: str | bytes, name: str) -> str:
    if isinstance(value, bytes):
        return value.decode("latin-1")
    if isinstance(value, str):
        return value
    raise TypeError(f"{name} must be str or bytes, not {type(value).__name__}.")


def verify_signature(
    payload: bytes,
    header: str | bytes | None,
    secret: str | bytes | Sequence[str | bytes],
    *,
    tolerance: int = TOLERANCE_SECONDS,
    now: float | None = None,
) -> None:
    """Raise `SignatureVerificationError` unless ``header`` (`X-Talki-Signature`,
    `t=<unix seconds>,v1=<hex>[,v1=…]`) signs ``payload`` with ``secret``
    (or one of several) within ``tolerance`` seconds of now.

    Any `v1` may match: during a rotation the header carries one per secret.
    """
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError("payload must be the body's bytes as received, not a decoded or re-serialised str.")
    if not header:
        raise SignatureVerificationError(f"No {SIGNATURE_HEADER} header.")
    header = _text(header, "header")
    given = [secret] if isinstance(secret, (str, bytes)) else list(secret)
    if not given or not all(given):
        raise ValueError("A signing secret is required.")
    # A str secret is the UTF-8 the server signs with; bytes are the key as is.
    keys = [key.encode() if isinstance(key, str) else bytes(key) for key in given]

    timestamp: str | None = None
    signatures: list[str] = []
    for part in header.split(","):
        name, _, value = part.strip().partition("=")
        if name == "t":
            timestamp = value
        elif name == "v1" and len(value) == _HEX_DIGEST_LENGTH and set(value) <= _HEX:
            # Only what could be an HMAC: anything else is no match, never a
            # crash on characters `compare_digest` will not take.
            signatures.append(value)
    if timestamp is None or not signatures:
        raise SignatureVerificationError(f"Malformed {SIGNATURE_HEADER} header.")
    try:
        signed_at = int(timestamp)
    except ValueError:
        raise SignatureVerificationError("The signature's timestamp is not an integer.") from None

    signed = timestamp.encode() + b"." + bytes(payload)
    expected = [hmac.new(key, signed, hashlib.sha256).hexdigest() for key in keys]
    if not any(hmac.compare_digest(want, got) for want in expected for got in signatures):
        raise SignatureVerificationError("The signature does not match.")

    # Checked after the HMAC, so a forged header cannot be told from a stale
    # one by how fast it is refused.
    # In integers: a float minus an int of 300+ digits would overflow.
    age = int(time.time() if now is None else now) - signed_at
    if abs(age) > tolerance:
        raise SignatureVerificationError(f"The signature is {int(abs(age))} s from now; refused as a possible replay.")


def construct_event(
    payload: bytes,
    header: str | bytes | None,
    secret: str | bytes | Sequence[str | bytes],
    *,
    tolerance: int = TOLERANCE_SECONDS,
    now: float | None = None,
) -> dict[str, Any]:
    """The event, once `verify_signature` passes: the envelope as a dict
    (`id`, `type`, `created_at`, `livemode`, `data`, …)."""
    verify_signature(payload, header, secret, tolerance=tolerance, now=now)
    try:
        event = json.loads(payload)
    except ValueError:
        raise SignatureVerificationError("The signed body is not JSON.") from None
    if not isinstance(event, dict):
        raise SignatureVerificationError("The signed body is not an event object.")
    return event
