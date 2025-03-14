# accent_bus/resources/line_endpoint/types.py
# Copyright 2025 Accent Communications

"""Line endpoint types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    """Dictionary representing auth section options for a SIP endpoint."""

    username: str


class LineEndpointSIPDict(TypedDict, total=False):
    """Dictionary representing a SIP line endpoint."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    label: str
    name: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict


class LineEndpointSCCPDict(TypedDict, total=False):
    """Dictionary representing an SCCP line endpoint."""

    id: int
    tenant_uuid: UUIDStr


class LineEndpointCustomDict(TypedDict, total=False):
    """Dictionary representing a custom line endpoint."""

    id: int
    tenant_uuid: UUIDStr
    interface: str


class LineDict(TypedDict, total=False):
    """Dictionary representing a line."""

    id: int
    tenant_uuid: UUIDStr
    name: str
