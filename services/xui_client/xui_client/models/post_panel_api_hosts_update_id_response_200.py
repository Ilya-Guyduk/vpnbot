from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.host import Host


T = TypeVar("T", bound="PostPanelApiHostsUpdateIdResponse200")


@_attrs_define
class PostPanelApiHostsUpdateIdResponse200:
    """
    Attributes:
        success (bool | Unset):
        msg (str | Unset):
        obj (Host | Unset): Host is an override endpoint attached to an inbound: at subscription time each
            enabled host renders one share link/proxy with its own address/port/TLS/etc.,
            superseding the legacy externalProxy array. Free-JSON fields are stored as
            text and parsed in the sub layer; slice fields use the json serializer.
    """

    success: bool | Unset = UNSET
    msg: str | Unset = UNSET
    obj: Host | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        msg = self.msg

        obj: dict[str, Any] | Unset = UNSET
        if not isinstance(self.obj, Unset):
            obj = self.obj.to_dict()

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
        from ..models.host import Host

        d = dict(src_dict)
        success = d.pop("success", UNSET)

        msg = d.pop("msg", UNSET)

        _obj = d.pop("obj", UNSET)
        obj: Host | Unset
        if isinstance(_obj, Unset):
            obj = UNSET
        else:
            obj = Host.from_dict(_obj)

        post_panel_api_hosts_update_id_response_200 = cls(
            success=success,
            msg=msg,
            obj=obj,
        )

        post_panel_api_hosts_update_id_response_200.additional_properties = d
        return post_panel_api_hosts_update_id_response_200

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
