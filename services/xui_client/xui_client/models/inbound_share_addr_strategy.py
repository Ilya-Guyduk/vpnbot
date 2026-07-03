from enum import Enum


class InboundShareAddrStrategy(str, Enum):
    CUSTOM = "custom"
    LISTEN = "listen"
    NODE = "node"

    def __str__(self) -> str:
        return str(self.value)
