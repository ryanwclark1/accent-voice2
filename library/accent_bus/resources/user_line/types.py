# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class EndpointCustomDict(TypedDict, total=False):
    id: int


class EndpointSCCPDict(TypedDict, total=False):
    id: int


class EndpointSIPDict(TypedDict, total=False):
    uuid: UUIDStr


class LineDict(TypedDict, total=False):
    id: int
    name: str
    endpoint_sip: EndpointSIPDict
    endpoint_sccp: EndpointSCCPDict
    endpoint_custom: EndpointCustomDict


class UserDict(TypedDict, total=False):
    id: int
    uuid: UUIDStr
    tenant_uuid: UUIDStr
