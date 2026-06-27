from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiTokenView")


@_attrs_define
class ApiTokenView:
    """
    Attributes:
        created_at (int):  Example: 1736000000.
        enabled (bool):  Example: True.
        id (int):  Example: 2.
        name (str):  Example: central-panel-a.
        token (str | Unset):  Example: new-token-string.
    """

    created_at: int
    enabled: bool
    id: int
    name: str
    token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        enabled = self.enabled

        id = self.id

        name = self.name

        token = self.token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "enabled": enabled,
                "id": id,
                "name": name,
            }
        )
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("createdAt")

        enabled = d.pop("enabled")

        id = d.pop("id")

        name = d.pop("name")

        token = d.pop("token", UNSET)

        api_token_view = cls(
            created_at=created_at,
            enabled=enabled,
            id=id,
            name=name,
            token=token,
        )

        api_token_view.additional_properties = d
        return api_token_view

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
