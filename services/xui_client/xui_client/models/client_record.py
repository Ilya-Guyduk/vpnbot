from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ClientRecord")


@_attrs_define
class ClientRecord:
    """
    Attributes:
        auth (str):
        comment (str):
        created_at (int):
        email (str):
        enable (bool):
        expiry_time (int):
        flow (str):
        group (str):
        id (int):
        limit_ip (int):
        password (str):
        reset (int):
        reverse (Any):
        security (str):
        sub_id (str):
        tg_id (int):
        total_gb (int):
        updated_at (int):
        uuid (str):
    """

    auth: str
    comment: str
    created_at: int
    email: str
    enable: bool
    expiry_time: int
    flow: str
    group: str
    id: int
    limit_ip: int
    password: str
    reset: int
    reverse: Any
    security: str
    sub_id: str
    tg_id: int
    total_gb: int
    updated_at: int
    uuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auth = self.auth

        comment = self.comment

        created_at = self.created_at

        email = self.email

        enable = self.enable

        expiry_time = self.expiry_time

        flow = self.flow

        group = self.group

        id = self.id

        limit_ip = self.limit_ip

        password = self.password

        reset = self.reset

        reverse = self.reverse

        security = self.security

        sub_id = self.sub_id

        tg_id = self.tg_id

        total_gb = self.total_gb

        updated_at = self.updated_at

        uuid = self.uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "auth": auth,
                "comment": comment,
                "createdAt": created_at,
                "email": email,
                "enable": enable,
                "expiryTime": expiry_time,
                "flow": flow,
                "group": group,
                "id": id,
                "limitIp": limit_ip,
                "password": password,
                "reset": reset,
                "reverse": reverse,
                "security": security,
                "subId": sub_id,
                "tgId": tg_id,
                "totalGB": total_gb,
                "updatedAt": updated_at,
                "uuid": uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auth = d.pop("auth")

        comment = d.pop("comment")

        created_at = d.pop("createdAt")

        email = d.pop("email")

        enable = d.pop("enable")

        expiry_time = d.pop("expiryTime")

        flow = d.pop("flow")

        group = d.pop("group")

        id = d.pop("id")

        limit_ip = d.pop("limitIp")

        password = d.pop("password")

        reset = d.pop("reset")

        reverse = d.pop("reverse")

        security = d.pop("security")

        sub_id = d.pop("subId")

        tg_id = d.pop("tgId")

        total_gb = d.pop("totalGB")

        updated_at = d.pop("updatedAt")

        uuid = d.pop("uuid")

        client_record = cls(
            auth=auth,
            comment=comment,
            created_at=created_at,
            email=email,
            enable=enable,
            expiry_time=expiry_time,
            flow=flow,
            group=group,
            id=id,
            limit_ip=limit_ip,
            password=password,
            reset=reset,
            reverse=reverse,
            security=security,
            sub_id=sub_id,
            tg_id=tg_id,
            total_gb=total_gb,
            updated_at=updated_at,
            uuid=uuid,
        )

        client_record.additional_properties = d
        return client_record

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
