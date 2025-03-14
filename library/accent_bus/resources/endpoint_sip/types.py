# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    username: str


class EndpointSIPLineDict(TypedDict, total=False):
    id: int


class EndpointSIPTrunkDict(TypedDict, total=False):
    id: int


class EndpointSIPRegistrationSectionOptionsDict(TypedDict, total=False):
    client_uri: str


class EndpointSIPDict(TypedDict, total=False):
    uuid: UUIDStr
    tenant_uuid: UUIDStr
    name: str
    label: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict
    regsitration_section_options: EndpointSIPRegistrationSectionOptionsDict
    trunk: EndpointSIPTrunkDict
    line: EndpointSIPLineDict
