from enum import IntEnum


class AccountCallAutoArchiveDaysType0(IntEnum):
    VALUE_7 = 7
    VALUE_30 = 30
    VALUE_90 = 90
    VALUE_180 = 180

    def __str__(self) -> str:
        return str(self.value)
