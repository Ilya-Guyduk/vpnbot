from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProbeResultUI")


@_attrs_define
class ProbeResultUI:
    """
    Attributes:
        cpu_pct (float):  Example: 12.5.
        error (str):
        latency_ms (int):  Example: 42.
        mem_pct (float):  Example: 45.2.
        panel_version (str):  Example: v3.x.x.
        status (str):  Example: online.
        uptime_secs (int):  Example: 86400.
        xray_error (str):
        xray_state (str): XrayState/XrayError are populated on successful probes even when the node's
            Xray core is not healthy. The UI uses them for a distinct "panel ok, xray failed" indicator.
        xray_version (str):  Example: 25.10.31.
    """

    cpu_pct: float
    error: str
    latency_ms: int
    mem_pct: float
    panel_version: str
    status: str
    uptime_secs: int
    xray_error: str
    xray_state: str
    xray_version: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu_pct = self.cpu_pct

        error = self.error

        latency_ms = self.latency_ms

        mem_pct = self.mem_pct

        panel_version = self.panel_version

        status = self.status

        uptime_secs = self.uptime_secs

        xray_error = self.xray_error

        xray_state = self.xray_state

        xray_version = self.xray_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cpuPct": cpu_pct,
                "error": error,
                "latencyMs": latency_ms,
                "memPct": mem_pct,
                "panelVersion": panel_version,
                "status": status,
                "uptimeSecs": uptime_secs,
                "xrayError": xray_error,
                "xrayState": xray_state,
                "xrayVersion": xray_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cpu_pct = d.pop("cpuPct")

        error = d.pop("error")

        latency_ms = d.pop("latencyMs")

        mem_pct = d.pop("memPct")

        panel_version = d.pop("panelVersion")

        status = d.pop("status")

        uptime_secs = d.pop("uptimeSecs")

        xray_error = d.pop("xrayError")

        xray_state = d.pop("xrayState")

        xray_version = d.pop("xrayVersion")

        probe_result_ui = cls(
            cpu_pct=cpu_pct,
            error=error,
            latency_ms=latency_ms,
            mem_pct=mem_pct,
            panel_version=panel_version,
            status=status,
            uptime_secs=uptime_secs,
            xray_error=xray_error,
            xray_state=xray_state,
            xray_version=xray_version,
        )

        probe_result_ui.additional_properties = d
        return probe_result_ui

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
