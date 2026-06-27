from enum import Enum


class InboundTrafficReset(str, Enum):
    DAILY = "daily"
    HOURLY = "hourly"
    MONTHLY = "monthly"
    NEVER = "never"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
