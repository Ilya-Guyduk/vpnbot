from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ClientTraffic")


@_attrs_define
class ClientTraffic:
    """ClientTraffic represents traffic statistics and limits for a specific client.
    It tracks upload/download usage, expiry times, and online status for inbound clients.

        Attributes:
            down (int):  Example: 2097152.
            email (str):  Example: user1.
            enable (bool):  Example: True.
            expiry_time (int):  Example: 1735689600000.
            id (int):  Example: 14825.
            inbound_id (int):  Example: 1.
            last_online (int):  Example: 1735680000000.
            reset (int):
            sub_id (str):  Example: i7tvdpeffi0hvvf1.
            total (int):  Example: 10737418240.
            up (int):  Example: 1048576.
            uuid (str):  Example: e18c9a96-71bf-48d4-933f-8b9a46d4290c.
    """

    down: int
    email: str
    enable: bool
    expiry_time: int
    id: int
    inbound_id: int
    last_online: int
    reset: int
    sub_id: str
    total: int
    up: int
    uuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        down = self.down

        email = self.email

        enable = self.enable

        expiry_time = self.expiry_time

        id = self.id

        inbound_id = self.inbound_id

        last_online = self.last_online

        reset = self.reset

        sub_id = self.sub_id

        total = self.total

        up = self.up

        uuid = self.uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "down": down,
                "email": email,
                "enable": enable,
                "expiryTime": expiry_time,
                "id": id,
                "inboundId": inbound_id,
                "lastOnline": last_online,
                "reset": reset,
                "subId": sub_id,
                "total": total,
                "up": up,
                "uuid": uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        down = d.pop("down")

        email = d.pop("email")

        enable = d.pop("enable")

        expiry_time = d.pop("expiryTime")

        id = d.pop("id")

        inbound_id = d.pop("inboundId")

        last_online = d.pop("lastOnline")

        reset = d.pop("reset")

        sub_id = d.pop("subId")

        total = d.pop("total")

        up = d.pop("up")

        uuid = d.pop("uuid")

        client_traffic = cls(
            down=down,
            email=email,
            enable=enable,
            expiry_time=expiry_time,
            id=id,
            inbound_id=inbound_id,
            last_online=last_online,
            reset=reset,
            sub_id=sub_id,
            total=total,
            up=up,
            uuid=uuid,
        )

        client_traffic.additional_properties = d
        return client_traffic

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
