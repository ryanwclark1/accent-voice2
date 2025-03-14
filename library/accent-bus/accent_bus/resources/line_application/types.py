# accent_bus/resources/line_application/types.py
# Copyright 2025 Accent Communications

"""Line application types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class ApplicationDict(TypedDict, total=False):
    """Dictionary representing an application."""

    uuid: UUIDStr


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
