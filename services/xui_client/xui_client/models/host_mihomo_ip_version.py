from enum import Enum


class HostMihomoIpVersion(str, Enum):
    DUAL = "dual"
    IPV4 = "ipv4"
    IPV4_PREFER = "ipv4-prefer"
    IPV6 = "ipv6"
    IPV6_PREFER = "ipv6-prefer"

    def __str__(self) -> str:
        return str(self.value)
