from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InboundOption")


@_attrs_define
class InboundOption:
    """
    Attributes:
        id (int):  Example: 1.
        port (int):  Example: 443.
        protocol (str):  Example: vless.
        remark (str):  Example: VLESS-443.
        ss_method (str):
        tag (str):  Example: in-443-tcp.
        tls_flow_capable (bool):  Example: True.
        node_id (int | None | Unset): Hosting node; nil for this panel's own inbounds. Lets the clients
            page map a node filter onto inbound IDs (#4997).
    """

    id: int
    port: int
    protocol: str
    remark: str
    ss_method: str
    tag: str
    tls_flow_capable: bool
    node_id: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        port = self.port

        protocol = self.protocol

        remark = self.remark

        ss_method = self.ss_method

        tag = self.tag

        tls_flow_capable = self.tls_flow_capable

        node_id: int | None | Unset
        if isinstance(self.node_id, Unset):
            node_id = UNSET
        else:
            node_id = self.node_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "port": port,
                "protocol": protocol,
                "remark": remark,
                "ssMethod": ss_method,
                "tag": tag,
                "tlsFlowCapable": tls_flow_capable,
            }
        )
        if node_id is not UNSET:
            field_dict["nodeId"] = node_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        port = d.pop("port")

        protocol = d.pop("protocol")

        remark = d.pop("remark")

        ss_method = d.pop("ssMethod")

        tag = d.pop("tag")

        tls_flow_capable = d.pop("tlsFlowCapable")

        def _parse_node_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        node_id = _parse_node_id(d.pop("nodeId", UNSET))

        inbound_option = cls(
            id=id,
            port=port,
            protocol=protocol,
            remark=remark,
            ss_method=ss_method,
            tag=tag,
            tls_flow_capable=tls_flow_capable,
            node_id=node_id,
        )

        inbound_option.additional_properties = d
        return inbound_option

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
