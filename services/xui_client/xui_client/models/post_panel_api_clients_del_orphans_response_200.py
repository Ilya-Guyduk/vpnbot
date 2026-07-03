from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostPanelApiClientsDelOrphansResponse200")


@_attrs_define
class PostPanelApiClientsDelOrphansResponse200:
    """
    Attributes:
        success (bool | Unset):
        msg (str | Unset):
        obj (Any | Unset):
    """

    success: bool | Unset = UNSET
    msg: str | Unset = UNSET
    obj: Any | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        msg = self.msg

        obj = self.obj

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if success is not UNSET:
            field_dict["success"] = success
        if msg is not UNSET:
            field_dict["msg"] = msg
        if obj is not UNSET:
            field_dict["obj"] = obj

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success = d.pop("success", UNSET)

        msg = d.pop("msg", UNSET)

        obj = d.pop("obj", UNSET)

        post_panel_api_clients_del_orphans_response_200 = cls(
            success=success,
            msg=msg,
            obj=obj,
        )

        post_panel_api_clients_del_orphans_response_200.additional_properties = d
        return post_panel_api_clients_del_orphans_response_200

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
