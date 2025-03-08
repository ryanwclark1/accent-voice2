# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class EndpointCustomLineDict(TypedDict, total=False):
    id: int


class EndpointCustomTrunkDict(TypedDict, total=False):
    id: int


class EndpointCustomDict(TypedDict, total=False):
    id: int
    tenant_uuid: UUIDStr
    interface: str
    trunk: EndpointCustomTrunkDict
    line: EndpointCustomLineDict
