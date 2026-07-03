from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FallbackParentInfo")


@_attrs_define
class FallbackParentInfo:
    """FallbackParentInfo carries everything the frontend needs to rewrite a
    child inbound's client link: where to connect (the master's address
    and port) and which path matched on the master's fallbacks array.
    The frontend already has the master inbound in its dbInbounds list,
    so we only ship identifiers + the match path here.

        Attributes:
            master_id (int):
            path (str | Unset):
    """

    master_id: int
    path: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        master_id = self.master_id

        path = self.path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "masterId": master_id,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        master_id = d.pop("masterId")

        path = d.pop("path", UNSET)

        fallback_parent_info = cls(
            master_id=master_id,
            path=path,
        )

        fallback_parent_info.additional_properties = d
        return fallback_parent_info

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
