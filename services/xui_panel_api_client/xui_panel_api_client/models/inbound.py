from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.inbound_protocol import InboundProtocol
from ..models.inbound_share_addr_strategy import InboundShareAddrStrategy
from ..models.inbound_traffic_reset import InboundTrafficReset
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.client_traffic import ClientTraffic
    from ..models.fallback_parent_info import FallbackParentInfo


T = TypeVar("T", bound="Inbound")


@_attrs_define
class Inbound:
    """Inbound represents an Xray inbound configuration with traffic statistics and settings.

    Attributes:
        client_stats (list[ClientTraffic]): Client traffic statistics
        down (int): Download traffic in bytes
        enable (bool): Whether the inbound is enabled Example: True.
        expiry_time (int): Expiration timestamp
        id (int): Unique identifier Example: 1.
        last_traffic_reset_time (int): Last traffic reset timestamp
        listen (str): Xray configuration fields
        port (int):  Example: 443.
        protocol (InboundProtocol):  Example: vless.
        remark (str): Human-readable remark Example: VLESS-443.
        settings (Any):
        share_addr (str):
        share_addr_strategy (InboundShareAddrStrategy):
        sniffing (Any):
        stream_settings (Any):
        sub_sort_index (int): 1-based sort order of this inbound's links in subscription output only (lower first; ties
            by id) Example: 1.
        tag (str):  Example: in-443-tcp.
        total (int): Total traffic limit in bytes
        traffic_reset (InboundTrafficReset): Traffic reset schedule
        up (int): Upload traffic in bytes
        fallback_parent (FallbackParentInfo | None | Unset): FallbackParent is populated by the API layer when this
            inbound is
            attached as a fallback child of a VLESS/Trojan TCP-TLS master.
            The frontend uses it to rewrite client-share links so they advertise
            the master's externally reachable endpoint instead of the child's
            loopback listen. Not persisted.
        node_id (int | None | Unset):
        origin_node_guid (str | Unset): OriginNodeGuid is the panelGuid of the node that physically hosts this
            inbound, propagated up across hops (#4983). Empty for an inbound that
            lives on this panel's own xray; set to the originating node's GUID when
            the inbound was synced from a node (kept as-is across further hops). Lets
            the master attribute a deeply nested inbound to the real node instead of
            the intermediate one it was fetched through.
    """

    client_stats: list[ClientTraffic]
    down: int
    enable: bool
    expiry_time: int
    id: int
    last_traffic_reset_time: int
    listen: str
    port: int
    protocol: InboundProtocol
    remark: str
    settings: Any
    share_addr: str
    share_addr_strategy: InboundShareAddrStrategy
    sniffing: Any
    stream_settings: Any
    sub_sort_index: int
    tag: str
    total: int
    traffic_reset: InboundTrafficReset
    up: int
    fallback_parent: FallbackParentInfo | None | Unset = UNSET
    node_id: int | None | Unset = UNSET
    origin_node_guid: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.fallback_parent_info import FallbackParentInfo

        client_stats = []
        for client_stats_item_data in self.client_stats:
            client_stats_item = client_stats_item_data.to_dict()
            client_stats.append(client_stats_item)

        down = self.down

        enable = self.enable

        expiry_time = self.expiry_time

        id = self.id

        last_traffic_reset_time = self.last_traffic_reset_time

        listen = self.listen

        port = self.port

        protocol = self.protocol.value

        remark = self.remark

        settings = self.settings

        share_addr = self.share_addr

        share_addr_strategy = self.share_addr_strategy.value

        sniffing = self.sniffing

        stream_settings = self.stream_settings

        sub_sort_index = self.sub_sort_index

        tag = self.tag

        total = self.total

        traffic_reset = self.traffic_reset.value

        up = self.up

        fallback_parent: dict[str, Any] | None | Unset
        if isinstance(self.fallback_parent, Unset):
            fallback_parent = UNSET
        elif isinstance(self.fallback_parent, FallbackParentInfo):
            fallback_parent = self.fallback_parent.to_dict()
        else:
            fallback_parent = self.fallback_parent

        node_id: int | None | Unset
        if isinstance(self.node_id, Unset):
            node_id = UNSET
        else:
            node_id = self.node_id

        origin_node_guid = self.origin_node_guid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "clientStats": client_stats,
                "down": down,
                "enable": enable,
                "expiryTime": expiry_time,
                "id": id,
                "lastTrafficResetTime": last_traffic_reset_time,
                "listen": listen,
                "port": port,
                "protocol": protocol,
                "remark": remark,
                "settings": settings,
                "shareAddr": share_addr,
                "shareAddrStrategy": share_addr_strategy,
                "sniffing": sniffing,
                "streamSettings": stream_settings,
                "subSortIndex": sub_sort_index,
                "tag": tag,
                "total": total,
                "trafficReset": traffic_reset,
                "up": up,
            }
        )
        if fallback_parent is not UNSET:
            field_dict["fallbackParent"] = fallback_parent
        if node_id is not UNSET:
            field_dict["nodeId"] = node_id
        if origin_node_guid is not UNSET:
            field_dict["originNodeGuid"] = origin_node_guid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.client_traffic import ClientTraffic
        from ..models.fallback_parent_info import FallbackParentInfo

        d = dict(src_dict)
        client_stats = []
        _client_stats = d.pop("clientStats")
        for client_stats_item_data in _client_stats:
            client_stats_item = ClientTraffic.from_dict(client_stats_item_data)

            client_stats.append(client_stats_item)

        down = d.pop("down")

        enable = d.pop("enable")

        expiry_time = d.pop("expiryTime")

        id = d.pop("id")

        last_traffic_reset_time = d.pop("lastTrafficResetTime")

        listen = d.pop("listen")

        port = d.pop("port")

        protocol = InboundProtocol(d.pop("protocol"))

        remark = d.pop("remark")

        settings = d.pop("settings")

        share_addr = d.pop("shareAddr")

        share_addr_strategy = InboundShareAddrStrategy(d.pop("shareAddrStrategy"))

        sniffing = d.pop("sniffing")

        stream_settings = d.pop("streamSettings")

        sub_sort_index = d.pop("subSortIndex")

        tag = d.pop("tag")

        total = d.pop("total")

        traffic_reset = InboundTrafficReset(d.pop("trafficReset"))

        up = d.pop("up")

        def _parse_fallback_parent(data: object) -> FallbackParentInfo | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fallback_parent_type_1 = FallbackParentInfo.from_dict(data)

                return fallback_parent_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FallbackParentInfo | None | Unset, data)

        fallback_parent = _parse_fallback_parent(d.pop("fallbackParent", UNSET))

        def _parse_node_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        node_id = _parse_node_id(d.pop("nodeId", UNSET))

        origin_node_guid = d.pop("originNodeGuid", UNSET)

        inbound = cls(
            client_stats=client_stats,
            down=down,
            enable=enable,
            expiry_time=expiry_time,
            id=id,
            last_traffic_reset_time=last_traffic_reset_time,
            listen=listen,
            port=port,
            protocol=protocol,
            remark=remark,
            settings=settings,
            share_addr=share_addr,
            share_addr_strategy=share_addr_strategy,
            sniffing=sniffing,
            stream_settings=stream_settings,
            sub_sort_index=sub_sort_index,
            tag=tag,
            total=total,
            traffic_reset=traffic_reset,
            up=up,
            fallback_parent=fallback_parent,
            node_id=node_id,
            origin_node_guid=origin_node_guid,
        )

        inbound.additional_properties = d
        return inbound

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
