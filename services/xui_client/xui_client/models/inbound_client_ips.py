from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InboundClientIps")


@_attrs_define
class InboundClientIps:
    """InboundClientIps stores IP addresses associated with inbound clients for access control.

    Attributes:
        client_email (str):
        id (int):
        ips (Any):
    """

    client_email: str
    id: int
    ips: Any
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_email = self.client_email

        id = self.id

        ips = self.ips

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "clientEmail": client_email,
                "id": id,
                "ips": ips,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_email = d.pop("clientEmail")

        id = d.pop("id")

        ips = d.pop("ips")

        inbound_client_ips = cls(
            client_email=client_email,
            id=id,
            ips=ips,
        )

        inbound_client_ips.additional_properties = d
        return inbound_client_ips

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
