# accent_bus/resources/trunk_endpoint/types.py
# Copyright 2025 Accent Communications

"""Trunk endpoint types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class EndpointSIPDict(TypedDict, total=False):
    """Dictionary representing a SIP endpoint."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    name: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict
    registration_section_options: EndpointSIPRegistrationSectionOptionsDict


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    """Dictionary representing auth section options for a SIP endpoint."""

    username: str


class EndpointSIPRegistrationSectionOptionsDict(TypedDict, total=False):
    """Dictionary representing registration section options for a SIP endpoint."""

    client_uri: str


class EndpointIAXDict(TypedDict, total=False):
    """Dictionary representing an IAX endpoint."""

    id: int
    tenant_uuid: UUIDStr
    name: str


class EndpointCustomDict(TypedDict, total=False):
    """Dictionary representing a custom endpoint."""

    id: int
    tenant_uuid: UUIDStr
    interface: str


class TrunkDict(TypedDict, total=False):
    """Dictionary representing a trunk."""

    id: int
    tenant_uuid: UUIDStr
