from enum import StrEnum
from typing import Any

# Values the API added after this client was generated, each parsed once, so
# the same value is always the same member.
_UNLISTED: dict[str, Any] = {}


class InboxStatus(StrEnum):
    ALL = "all"
    ARCHIVED = "archived"
    INBOX = "inbox"
    UNREAD = "unread"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> Any:
        """A value the API added after this client was generated.

        It parses as a member not in the list above, named like one and equal
        to its string, so a response carrying it is read rather than refused.
        Compare against the string, and treat a value you do not handle as
        unknown.
        """
        if not isinstance(value, str):
            return None
        known = _UNLISTED.get(value)
        if known is not None:
            return known
        member = str.__new__(cls, value)
        member._name_ = value.upper()
        member._value_ = value
        # setdefault: of two threads parsing it at once, both get the first.
        return _UNLISTED.setdefault(value, member)
