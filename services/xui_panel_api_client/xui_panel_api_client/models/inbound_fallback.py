from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InboundFallback")


@_attrs_define
class InboundFallback:
    """
    Attributes:
        alpn (str):
        child_id (int):
        dest (str):
        id (int):
        master_id (int):
        name (str):
        path (str):
        sort_order (int):
        xver (int):
    """

    alpn: str
    child_id: int
    dest: str
    id: int
    master_id: int
    name: str
    path: str
    sort_order: int
    xver: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alpn = self.alpn

        child_id = self.child_id

        dest = self.dest

        id = self.id

        master_id = self.master_id

        name = self.name

        path = self.path

        sort_order = self.sort_order

        xver = self.xver

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "alpn": alpn,
                "childId": child_id,
                "dest": dest,
                "id": id,
                "masterId": master_id,
                "name": name,
                "path": path,
                "sortOrder": sort_order,
                "xver": xver,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        alpn = d.pop("alpn")

        child_id = d.pop("childId")

        dest = d.pop("dest")

        id = d.pop("id")

        master_id = d.pop("masterId")

        name = d.pop("name")

        path = d.pop("path")

        sort_order = d.pop("sortOrder")

        xver = d.pop("xver")

        inbound_fallback = cls(
            alpn=alpn,
            child_id=child_id,
            dest=dest,
            id=id,
            master_id=master_id,
            name=name,
            path=path,
            sort_order=sort_order,
            xver=xver,
        )

        inbound_fallback.additional_properties = d
        return inbound_fallback

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
