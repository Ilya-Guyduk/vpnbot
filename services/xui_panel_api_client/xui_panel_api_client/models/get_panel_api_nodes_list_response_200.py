from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.node import Node


T = TypeVar("T", bound="GetPanelApiNodesListResponse200")


@_attrs_define
class GetPanelApiNodesListResponse200:
    """
    Attributes:
        success (bool | Unset):
        msg (str | Unset):
        obj (list[Node] | Unset):
    """

    success: bool | Unset = UNSET
    msg: str | Unset = UNSET
    obj: list[Node] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        msg = self.msg

        obj: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.obj, Unset):
            obj = []
            for obj_item_data in self.obj:
                obj_item = obj_item_data.to_dict()
                obj.append(obj_item)

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
        from ..models.node import Node

        d = dict(src_dict)
        success = d.pop("success", UNSET)

        msg = d.pop("msg", UNSET)

        _obj = d.pop("obj", UNSET)
        obj: list[Node] | Unset = UNSET
        if _obj is not UNSET:
            obj = []
            for obj_item_data in _obj:
                obj_item = Node.from_dict(obj_item_data)

                obj.append(obj_item)

        get_panel_api_nodes_list_response_200 = cls(
            success=success,
            msg=msg,
            obj=obj,
        )

        get_panel_api_nodes_list_response_200.additional_properties = d
        return get_panel_api_nodes_list_response_200

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
