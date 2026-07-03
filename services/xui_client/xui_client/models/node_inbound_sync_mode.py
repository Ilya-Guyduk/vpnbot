from enum import Enum


class NodeInboundSyncMode(str, Enum):
    ALL = "all"
    SELECTED = "selected"

    def __str__(self) -> str:
        return str(self.value)
