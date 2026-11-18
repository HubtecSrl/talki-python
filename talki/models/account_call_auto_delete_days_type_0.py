from enum import IntEnum


class AccountCallAutoDeleteDaysType0(IntEnum):
    VALUE_30 = 30
    VALUE_60 = 60
    VALUE_90 = 90
    VALUE_180 = 180

    def __str__(self) -> str:
        return str(self.value)
