# accent_bus/resources/user_line/types.py
# Copyright 2025 Accent Communications

"""User line types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class EndpointCustomDict(TypedDict, total=False):
    """Dictionary representing a custom endpoint."""

    id: int


class EndpointSCCPDict(TypedDict, total=False):
    """Dictionary representing an SCCP endpoint."""

    id: int


class EndpointSIPDict(TypedDict, total=False):
    """Dictionary representing a SIP endpoint."""

    uuid: UUIDStr


class LineDict(TypedDict, total=False):
    """Dictionary representing a line."""

    id: int
    name: str
    endpoint_sip: EndpointSIPDict
    endpoint_sccp: EndpointSCCPDict
    endpoint_custom: EndpointCustomDict


class UserDict(TypedDict, total=False):
    """Dictionary representing a user."""

    id: int
    uuid: UUIDStr
    tenant_uuid: UUIDStr
