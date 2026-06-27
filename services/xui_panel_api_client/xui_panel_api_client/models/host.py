from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.host_mihomo_ip_version import HostMihomoIpVersion
from ..models.host_security import HostSecurity
from ..types import UNSET, Unset

T = TypeVar("T", bound="Host")


@_attrs_define
class Host:
    """Host is an override endpoint attached to an inbound: at subscription time each
    enabled host renders one share link/proxy with its own address/port/TLS/etc.,
    superseding the legacy externalProxy array. Free-JSON fields are stored as
    text and parsed in the sub layer; slice fields use the json serializer.

        Attributes:
            address (str):  Example: cdn.example.com.
            allow_insecure (bool):
            alpn (list[str]):
            created_at (int):
            ech_config_list (str):
            exclude_from_sub_types (list[str]):
            final_mask (str): FinalMask is a JSON object of xray finalmask masks (tcp/udp/quicParams),
                merged into this host's JSON-subscription stream. Empty = no override.
            fingerprint (str):
            host_header (str):
            id (int):  Example: 1.
            inbound_id (int):  Example: 1.
            is_disabled (bool):
            is_hidden (bool):
            keep_sni_blank (bool):
            mihomo_ip_version (HostMihomoIpVersion):
            mihomo_x25519 (bool):
            mux_params (Any):
            override_sni_from_address (bool):
            path (str):
            pinned_peer_cert_sha_256 (list[str]):
            port (int):  Example: 8443.
            remark (str):  Example: cdn-front.
            security (HostSecurity):  Example: same.
            server_description (str):
            shuffle_host (bool):
            sni (str):
            sockopt_params (Any):
            sort_order (int):
            tags (list[str]):
            updated_at (int):
            verify_peer_cert_by_name (str):
            vless_route (str): VlessRoute is a free-form port/range routing spec (e.g. "53,443,1000-2000");
                stored verbatim, format-validated on the frontend.
            node_guids (list[str] | Unset):
    """

    address: str
    allow_insecure: bool
    alpn: list[str]
    created_at: int
    ech_config_list: str
    exclude_from_sub_types: list[str]
    final_mask: str
    fingerprint: str
    host_header: str
    id: int
    inbound_id: int
    is_disabled: bool
    is_hidden: bool
    keep_sni_blank: bool
    mihomo_ip_version: HostMihomoIpVersion
    mihomo_x25519: bool
    mux_params: Any
    override_sni_from_address: bool
    path: str
    pinned_peer_cert_sha_256: list[str]
    port: int
    remark: str
    security: HostSecurity
    server_description: str
    shuffle_host: bool
    sni: str
    sockopt_params: Any
    sort_order: int
    tags: list[str]
    updated_at: int
    verify_peer_cert_by_name: str
    vless_route: str
    node_guids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address = self.address

        allow_insecure = self.allow_insecure

        alpn = self.alpn

        created_at = self.created_at

        ech_config_list = self.ech_config_list

        exclude_from_sub_types = self.exclude_from_sub_types

        final_mask = self.final_mask

        fingerprint = self.fingerprint

        host_header = self.host_header

        id = self.id

        inbound_id = self.inbound_id

        is_disabled = self.is_disabled

        is_hidden = self.is_hidden

        keep_sni_blank = self.keep_sni_blank

        mihomo_ip_version = self.mihomo_ip_version.value

        mihomo_x25519 = self.mihomo_x25519

        mux_params = self.mux_params

        override_sni_from_address = self.override_sni_from_address

        path = self.path

        pinned_peer_cert_sha_256 = self.pinned_peer_cert_sha_256

        port = self.port

        remark = self.remark

        security = self.security.value

        server_description = self.server_description

        shuffle_host = self.shuffle_host

        sni = self.sni

        sockopt_params = self.sockopt_params

        sort_order = self.sort_order

        tags = self.tags

        updated_at = self.updated_at

        verify_peer_cert_by_name = self.verify_peer_cert_by_name

        vless_route = self.vless_route

        node_guids: list[str] | Unset = UNSET
        if not isinstance(self.node_guids, Unset):
            node_guids = self.node_guids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "allowInsecure": allow_insecure,
                "alpn": alpn,
                "createdAt": created_at,
                "echConfigList": ech_config_list,
                "excludeFromSubTypes": exclude_from_sub_types,
                "finalMask": final_mask,
                "fingerprint": fingerprint,
                "hostHeader": host_header,
                "id": id,
                "inboundId": inbound_id,
                "isDisabled": is_disabled,
                "isHidden": is_hidden,
                "keepSniBlank": keep_sni_blank,
                "mihomoIpVersion": mihomo_ip_version,
                "mihomoX25519": mihomo_x25519,
                "muxParams": mux_params,
                "overrideSniFromAddress": override_sni_from_address,
                "path": path,
                "pinnedPeerCertSha256": pinned_peer_cert_sha_256,
                "port": port,
                "remark": remark,
                "security": security,
                "serverDescription": server_description,
                "shuffleHost": shuffle_host,
                "sni": sni,
                "sockoptParams": sockopt_params,
                "sortOrder": sort_order,
                "tags": tags,
                "updatedAt": updated_at,
                "verifyPeerCertByName": verify_peer_cert_by_name,
                "vlessRoute": vless_route,
            }
        )
        if node_guids is not UNSET:
            field_dict["nodeGuids"] = node_guids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        address = d.pop("address")

        allow_insecure = d.pop("allowInsecure")

        alpn = cast(list[str], d.pop("alpn"))

        created_at = d.pop("createdAt")

        ech_config_list = d.pop("echConfigList")

        exclude_from_sub_types = cast(list[str], d.pop("excludeFromSubTypes"))

        final_mask = d.pop("finalMask")

        fingerprint = d.pop("fingerprint")

        host_header = d.pop("hostHeader")

        id = d.pop("id")

        inbound_id = d.pop("inboundId")

        is_disabled = d.pop("isDisabled")

        is_hidden = d.pop("isHidden")

        keep_sni_blank = d.pop("keepSniBlank")

        mihomo_ip_version = HostMihomoIpVersion(d.pop("mihomoIpVersion"))

        mihomo_x25519 = d.pop("mihomoX25519")

        mux_params = d.pop("muxParams")

        override_sni_from_address = d.pop("overrideSniFromAddress")

        path = d.pop("path")

        pinned_peer_cert_sha_256 = cast(list[str], d.pop("pinnedPeerCertSha256"))

        port = d.pop("port")

        remark = d.pop("remark")

        security = HostSecurity(d.pop("security"))

        server_description = d.pop("serverDescription")

        shuffle_host = d.pop("shuffleHost")

        sni = d.pop("sni")

        sockopt_params = d.pop("sockoptParams")

        sort_order = d.pop("sortOrder")

        tags = cast(list[str], d.pop("tags"))

        updated_at = d.pop("updatedAt")

        verify_peer_cert_by_name = d.pop("verifyPeerCertByName")

        vless_route = d.pop("vlessRoute")

        node_guids = cast(list[str], d.pop("nodeGuids", UNSET))

        host = cls(
            address=address,
            allow_insecure=allow_insecure,
            alpn=alpn,
            created_at=created_at,
            ech_config_list=ech_config_list,
            exclude_from_sub_types=exclude_from_sub_types,
            final_mask=final_mask,
            fingerprint=fingerprint,
            host_header=host_header,
            id=id,
            inbound_id=inbound_id,
            is_disabled=is_disabled,
            is_hidden=is_hidden,
            keep_sni_blank=keep_sni_blank,
            mihomo_ip_version=mihomo_ip_version,
            mihomo_x25519=mihomo_x25519,
            mux_params=mux_params,
            override_sni_from_address=override_sni_from_address,
            path=path,
            pinned_peer_cert_sha_256=pinned_peer_cert_sha_256,
            port=port,
            remark=remark,
            security=security,
            server_description=server_description,
            shuffle_host=shuffle_host,
            sni=sni,
            sockopt_params=sockopt_params,
            sort_order=sort_order,
            tags=tags,
            updated_at=updated_at,
            verify_peer_cert_by_name=verify_peer_cert_by_name,
            vless_route=vless_route,
            node_guids=node_guids,
        )

        host.additional_properties = d
        return host

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
