from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_inbound_sync_mode import NodeInboundSyncMode
from ..models.node_scheme import NodeScheme
from ..models.node_tls_verify_mode import NodeTlsVerifyMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="Node")


@_attrs_define
class Node:
    """Node represents a remote 3x-ui panel registered with the central panel.
    The central panel polls each node's existing /panel/api/server/status
    endpoint over HTTP using the per-node ApiToken to populate the runtime
    status fields below.

        Attributes:
            active_count (int):  Example: 23.
            address (str):  Example: node1.example.com.
            allow_private_address (bool):
            api_token (str):  Example: abcdef0123456789.
            base_path (str):  Example: /.
            client_count (int):  Example: 27.
            config_dirty (bool):
            config_dirty_at (int):
            cpu_pct (float):  Example: 23.5.
            created_at (int):  Example: 1700000000.
            depleted_count (int):  Example: 1.
            disabled_count (int):  Example: 3.
            enable (bool):  Example: True.
            guid (str): Guid is the remote panel's stable self-identifier (its panelGuid),
                learned from each heartbeat. It is the globally stable node identity used
                to attribute online clients/inbounds to the physical node across a chain
                of nodes (#4983); panel-local autoincrement ids don't survive a hop.
                Observed-state only — never user-edited.
            id (int):  Example: 1.
            inbound_count (int):  Example: 5.
            inbound_sync_mode (NodeInboundSyncMode):
            inbound_tags (list[str]):
            last_error (str):
            last_heartbeat (int): unix seconds, 0 = never Example: 1700000000.
            latency_ms (int):  Example: 42.
            mem_pct (float):  Example: 45.1.
            name (str):  Example: de-fra-1.
            net_down (int):  Example: 2097152.
            net_up (int):  Example: 1048576.
            online_count (int):  Example: 3.
            outbound_tag (str):
            panel_version (str):  Example: v3.x.x.
            pinned_cert_sha_256 (str):
            port (int):  Example: 2053.
            remark (str):
            scheme (NodeScheme):  Example: https.
            status (str): Heartbeat-updated fields. UpdatedAt advances on every probe even when
                the row is otherwise unchanged so the UI's "last seen" tooltip is
                truthful without us having to read LastHeartbeat separately.
                online|offline|unknown Example: online.
            tls_verify_mode (NodeTlsVerifyMode):
            updated_at (int):  Example: 1700000000.
            uptime_secs (int):  Example: 86400.
            xray_error (str):
            xray_state (str): XrayState and XrayError are captured from the remote node's /panel/api/server/status
                during heartbeats. They let the central panel distinguish "panel API reachable"
                (status=online) from "Xray core itself has failed on the node" for monitoring.
            xray_version (str):  Example: 25.10.31.
            parent_guid (str | Unset): ParentGuid + Transitive are set only when a node is surfaced as part of a
                node tree (#4983): direct nodes carry the master panel's own GUID, a
                transitive sub-node carries its parent node's GUID. Transitive nodes are
                read-only projections (Id == 0, not persisted) — never edited or deployed.
            transitive (bool | Unset):
    """

    active_count: int
    address: str
    allow_private_address: bool
    api_token: str
    base_path: str
    client_count: int
    config_dirty: bool
    config_dirty_at: int
    cpu_pct: float
    created_at: int
    depleted_count: int
    disabled_count: int
    enable: bool
    guid: str
    id: int
    inbound_count: int
    inbound_sync_mode: NodeInboundSyncMode
    inbound_tags: list[str]
    last_error: str
    last_heartbeat: int
    latency_ms: int
    mem_pct: float
    name: str
    net_down: int
    net_up: int
    online_count: int
    outbound_tag: str
    panel_version: str
    pinned_cert_sha_256: str
    port: int
    remark: str
    scheme: NodeScheme
    status: str
    tls_verify_mode: NodeTlsVerifyMode
    updated_at: int
    uptime_secs: int
    xray_error: str
    xray_state: str
    xray_version: str
    parent_guid: str | Unset = UNSET
    transitive: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active_count = self.active_count

        address = self.address

        allow_private_address = self.allow_private_address

        api_token = self.api_token

        base_path = self.base_path

        client_count = self.client_count

        config_dirty = self.config_dirty

        config_dirty_at = self.config_dirty_at

        cpu_pct = self.cpu_pct

        created_at = self.created_at

        depleted_count = self.depleted_count

        disabled_count = self.disabled_count

        enable = self.enable

        guid = self.guid

        id = self.id

        inbound_count = self.inbound_count

        inbound_sync_mode = self.inbound_sync_mode.value

        inbound_tags = self.inbound_tags

        last_error = self.last_error

        last_heartbeat = self.last_heartbeat

        latency_ms = self.latency_ms

        mem_pct = self.mem_pct

        name = self.name

        net_down = self.net_down

        net_up = self.net_up

        online_count = self.online_count

        outbound_tag = self.outbound_tag

        panel_version = self.panel_version

        pinned_cert_sha_256 = self.pinned_cert_sha_256

        port = self.port

        remark = self.remark

        scheme = self.scheme.value

        status = self.status

        tls_verify_mode = self.tls_verify_mode.value

        updated_at = self.updated_at

        uptime_secs = self.uptime_secs

        xray_error = self.xray_error

        xray_state = self.xray_state

        xray_version = self.xray_version

        parent_guid = self.parent_guid

        transitive = self.transitive

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "activeCount": active_count,
                "address": address,
                "allowPrivateAddress": allow_private_address,
                "apiToken": api_token,
                "basePath": base_path,
                "clientCount": client_count,
                "configDirty": config_dirty,
                "configDirtyAt": config_dirty_at,
                "cpuPct": cpu_pct,
                "createdAt": created_at,
                "depletedCount": depleted_count,
                "disabledCount": disabled_count,
                "enable": enable,
                "guid": guid,
                "id": id,
                "inboundCount": inbound_count,
                "inboundSyncMode": inbound_sync_mode,
                "inboundTags": inbound_tags,
                "lastError": last_error,
                "lastHeartbeat": last_heartbeat,
                "latencyMs": latency_ms,
                "memPct": mem_pct,
                "name": name,
                "netDown": net_down,
                "netUp": net_up,
                "onlineCount": online_count,
                "outboundTag": outbound_tag,
                "panelVersion": panel_version,
                "pinnedCertSha256": pinned_cert_sha_256,
                "port": port,
                "remark": remark,
                "scheme": scheme,
                "status": status,
                "tlsVerifyMode": tls_verify_mode,
                "updatedAt": updated_at,
                "uptimeSecs": uptime_secs,
                "xrayError": xray_error,
                "xrayState": xray_state,
                "xrayVersion": xray_version,
            }
        )
        if parent_guid is not UNSET:
            field_dict["parentGuid"] = parent_guid
        if transitive is not UNSET:
            field_dict["transitive"] = transitive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active_count = d.pop("activeCount")

        address = d.pop("address")

        allow_private_address = d.pop("allowPrivateAddress")

        api_token = d.pop("apiToken")

        base_path = d.pop("basePath")

        client_count = d.pop("clientCount")

        config_dirty = d.pop("configDirty")

        config_dirty_at = d.pop("configDirtyAt")

        cpu_pct = d.pop("cpuPct")

        created_at = d.pop("createdAt")

        depleted_count = d.pop("depletedCount")

        disabled_count = d.pop("disabledCount")

        enable = d.pop("enable")

        guid = d.pop("guid")

        id = d.pop("id")

        inbound_count = d.pop("inboundCount")

        inbound_sync_mode = NodeInboundSyncMode(d.pop("inboundSyncMode"))

        inbound_tags = cast(list[str], d.pop("inboundTags"))

        last_error = d.pop("lastError")

        last_heartbeat = d.pop("lastHeartbeat")

        latency_ms = d.pop("latencyMs")

        mem_pct = d.pop("memPct")

        name = d.pop("name")

        net_down = d.pop("netDown")

        net_up = d.pop("netUp")

        online_count = d.pop("onlineCount")

        outbound_tag = d.pop("outboundTag")

        panel_version = d.pop("panelVersion")

        pinned_cert_sha_256 = d.pop("pinnedCertSha256")

        port = d.pop("port")

        remark = d.pop("remark")

        scheme = NodeScheme(d.pop("scheme"))

        status = d.pop("status")

        tls_verify_mode = NodeTlsVerifyMode(d.pop("tlsVerifyMode"))

        updated_at = d.pop("updatedAt")

        uptime_secs = d.pop("uptimeSecs")

        xray_error = d.pop("xrayError")

        xray_state = d.pop("xrayState")

        xray_version = d.pop("xrayVersion")

        parent_guid = d.pop("parentGuid", UNSET)

        transitive = d.pop("transitive", UNSET)

        node = cls(
            active_count=active_count,
            address=address,
            allow_private_address=allow_private_address,
            api_token=api_token,
            base_path=base_path,
            client_count=client_count,
            config_dirty=config_dirty,
            config_dirty_at=config_dirty_at,
            cpu_pct=cpu_pct,
            created_at=created_at,
            depleted_count=depleted_count,
            disabled_count=disabled_count,
            enable=enable,
            guid=guid,
            id=id,
            inbound_count=inbound_count,
            inbound_sync_mode=inbound_sync_mode,
            inbound_tags=inbound_tags,
            last_error=last_error,
            last_heartbeat=last_heartbeat,
            latency_ms=latency_ms,
            mem_pct=mem_pct,
            name=name,
            net_down=net_down,
            net_up=net_up,
            online_count=online_count,
            outbound_tag=outbound_tag,
            panel_version=panel_version,
            pinned_cert_sha_256=pinned_cert_sha_256,
            port=port,
            remark=remark,
            scheme=scheme,
            status=status,
            tls_verify_mode=tls_verify_mode,
            updated_at=updated_at,
            uptime_secs=uptime_secs,
            xray_error=xray_error,
            xray_state=xray_state,
            xray_version=xray_version,
            parent_guid=parent_guid,
            transitive=transitive,
        )

        node.additional_properties = d
        return node

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
