from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.client_reverse import ClientReverse


T = TypeVar("T", bound="Client")


@_attrs_define
class Client:
    """Client represents a client configuration for Xray inbounds with traffic limits and settings.

    Attributes:
        comment (str): Client comment
        email (str): Client email identifier
        enable (bool): Whether the client is enabled
        expiry_time (int): Expiration timestamp
        limit_ip (int): IP limit for this client
        reset (int): Reset period in days
        security (str): Security method (e.g., "auto", "aes-128-gcm")
        sub_id (str): Subscription identifier
        tg_id (int): Telegram user ID for notifications
        total_gb (int): Total traffic limit in GB
        auth (str | Unset): Auth password (Hysteria)
        created_at (int | Unset): Creation timestamp
        flow (str | Unset): Flow control (XTLS)
        group (str | Unset): Logical grouping label
        id (str | Unset): Unique client identifier
        password (str | Unset): Client password
        reverse (ClientReverse | None | Unset): VLESS simple reverse proxy settings
        updated_at (int | Unset): Last update timestamp
    """

    comment: str
    email: str
    enable: bool
    expiry_time: int
    limit_ip: int
    reset: int
    security: str
    sub_id: str
    tg_id: int
    total_gb: int
    auth: str | Unset = UNSET
    created_at: int | Unset = UNSET
    flow: str | Unset = UNSET
    group: str | Unset = UNSET
    id: str | Unset = UNSET
    password: str | Unset = UNSET
    reverse: ClientReverse | None | Unset = UNSET
    updated_at: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.client_reverse import ClientReverse

        comment = self.comment

        email = self.email

        enable = self.enable

        expiry_time = self.expiry_time

        limit_ip = self.limit_ip

        reset = self.reset

        security = self.security

        sub_id = self.sub_id

        tg_id = self.tg_id

        total_gb = self.total_gb

        auth = self.auth

        created_at = self.created_at

        flow = self.flow

        group = self.group

        id = self.id

        password = self.password

        reverse: dict[str, Any] | None | Unset
        if isinstance(self.reverse, Unset):
            reverse = UNSET
        elif isinstance(self.reverse, ClientReverse):
            reverse = self.reverse.to_dict()
        else:
            reverse = self.reverse

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "comment": comment,
                "email": email,
                "enable": enable,
                "expiryTime": expiry_time,
                "limitIp": limit_ip,
                "reset": reset,
                "security": security,
                "subId": sub_id,
                "tgId": tg_id,
                "totalGB": total_gb,
            }
        )
        if auth is not UNSET:
            field_dict["auth"] = auth
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if flow is not UNSET:
            field_dict["flow"] = flow
        if group is not UNSET:
            field_dict["group"] = group
        if id is not UNSET:
            field_dict["id"] = id
        if password is not UNSET:
            field_dict["password"] = password
        if reverse is not UNSET:
            field_dict["reverse"] = reverse
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.client_reverse import ClientReverse

        d = dict(src_dict)
        comment = d.pop("comment")

        email = d.pop("email")

        enable = d.pop("enable")

        expiry_time = d.pop("expiryTime")

        limit_ip = d.pop("limitIp")

        reset = d.pop("reset")

        security = d.pop("security")

        sub_id = d.pop("subId")

        tg_id = d.pop("tgId")

        total_gb = d.pop("totalGB")

        auth = d.pop("auth", UNSET)

        created_at = d.pop("created_at", UNSET)

        flow = d.pop("flow", UNSET)

        group = d.pop("group", UNSET)

        id = d.pop("id", UNSET)

        password = d.pop("password", UNSET)

        def _parse_reverse(data: object) -> ClientReverse | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                reverse_type_1 = ClientReverse.from_dict(data)

                return reverse_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ClientReverse | None | Unset, data)

        reverse = _parse_reverse(d.pop("reverse", UNSET))

        updated_at = d.pop("updated_at", UNSET)

        client = cls(
            comment=comment,
            email=email,
            enable=enable,
            expiry_time=expiry_time,
            limit_ip=limit_ip,
            reset=reset,
            security=security,
            sub_id=sub_id,
            tg_id=tg_id,
            total_gb=total_gb,
            auth=auth,
            created_at=created_at,
            flow=flow,
            group=group,
            id=id,
            password=password,
            reverse=reverse,
            updated_at=updated_at,
        )

        client.additional_properties = d
        return client

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
