from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OutboundTraffics")


@_attrs_define
class OutboundTraffics:
    """OutboundTraffics tracks traffic statistics for Xray outbound connections.

    Attributes:
        down (int):
        id (int):
        tag (str):
        total (int):
        up (int):
    """

    down: int
    id: int
    tag: str
    total: int
    up: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        down = self.down

        id = self.id

        tag = self.tag

        total = self.total

        up = self.up

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "down": down,
                "id": id,
                "tag": tag,
                "total": total,
                "up": up,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        down = d.pop("down")

        id = d.pop("id")

        tag = d.pop("tag")

        total = d.pop("total")

        up = d.pop("up")

        outbound_traffics = cls(
            down=down,
            id=id,
            tag=tag,
            total=total,
            up=up,
        )

        outbound_traffics.additional_properties = d
        return outbound_traffics

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
