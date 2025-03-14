# accent_bus/resources/line_device/types.py
# Copyright 2025 Accent Communications

"""Line device types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class DeviceDict(TypedDict, total=False):
    """Dictionary representing a device."""

    id: str


class LineEndpointSIPDict(TypedDict, total=False):
    """Dictionary representing a SIP line endpoint."""

    uuid: UUIDStr


class LineEndpointSCCPDict(TypedDict, total=False):
    """Dictionary representing an SCCP line endpoint."""

    id: int


class LineEndpointCustomDict(TypedDict, total=False):
    """Dictionary representing a custom line endpoint."""

    id: int


class LineDict(TypedDict, total=False):
    """Dictionary representing a line."""

    id: int
    name: str
    endpoint_sip: LineEndpointSIPDict
    endpoint_sccp: LineEndpointSCCPDict
    endpoint_custom: LineEndpointCustomDict
