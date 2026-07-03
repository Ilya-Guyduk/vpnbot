from enum import Enum


class NodeTlsVerifyMode(str, Enum):
    MTLS = "mtls"
    PIN = "pin"
    SKIP = "skip"
    VERIFY = "verify"

    def __str__(self) -> str:
        return str(self.value)
