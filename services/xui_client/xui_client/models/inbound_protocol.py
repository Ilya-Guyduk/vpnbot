from enum import Enum


class InboundProtocol(str, Enum):
    HTTP = "http"
    HYSTERIA = "hysteria"
    MIXED = "mixed"
    MTPROTO = "mtproto"
    SHADOWSOCKS = "shadowsocks"
    TROJAN = "trojan"
    TUN = "tun"
    TUNNEL = "tunnel"
    VLESS = "vless"
    VMESS = "vmess"
    WIREGUARD = "wireguard"

    def __str__(self) -> str:
        return str(self.value)
