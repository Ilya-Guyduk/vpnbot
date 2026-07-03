from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PostLoginBody")


@_attrs_define
class PostLoginBody:
    """
    Attributes:
        username (str): Panel admin username.
        password (str): Panel admin password.
        two_factor_code (str): OTP code when 2FA is enabled. Omit otherwise.
    """

    username: str
    password: str
    two_factor_code: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        password = self.password

        two_factor_code = self.two_factor_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "password": password,
                "twoFactorCode": two_factor_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        password = d.pop("password")

        two_factor_code = d.pop("twoFactorCode")

        post_login_body = cls(
            username=username,
            password=password,
            two_factor_code=two_factor_code,
        )

        post_login_body.additional_properties = d
        return post_login_body

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
