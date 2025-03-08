# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    username: str


class LineEndpointSIPDict(TypedDict, total=False):
    uuid: UUIDStr
    tenant_uuid: UUIDStr
    label: str
    name: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict


class LineEndpointSCCPDict(TypedDict, total=False):
    id: int
    tenant_uuid: UUIDStr


class LineEndpointCustomDict(TypedDict, total=False):
    id: int
    tenant_uuid: UUIDStr
    interface: str


class LineDict(TypedDict, total=False):
    id: int
    tenant_uuid: UUIDStr
    name: str
