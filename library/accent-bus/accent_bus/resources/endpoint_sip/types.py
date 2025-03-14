# accent_bus/resources/endpoint_sip/types.py
# Copyright 2025 Accent Communications

"""SIP endpoint types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    """Dictionary representing auth section options for a SIP endpoint."""

    username: str


class EndpointSIPLineDict(TypedDict, total=False):
    """Dictionary representing a SIP endpoint line."""

    id: int


class EndpointSIPTrunkDict(TypedDict, total=False):
    """Dictionary representing a SIP endpoint trunk."""

    id: int


class EndpointSIPRegistrationSectionOptionsDict(TypedDict, total=False):
    """Dictionary representing registration section options for a SIP endpoint."""

    client_uri: str


class EndpointSIPDict(TypedDict, total=False):
    """Dictionary representing a SIP endpoint."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    name: str
    label: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict
    regsitration_section_options: EndpointSIPRegistrationSectionOptionsDict
    trunk: EndpointSIPTrunkDict
    line: EndpointSIPLineDict
