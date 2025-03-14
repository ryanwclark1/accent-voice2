# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class EndpointSCCPLineDict(TypedDict, total=False):
    id: int


class EndpointSCCPDict(TypedDict, total=False):
    id: int
    tenant_uuid: UUIDStr
    line: EndpointSCCPLineDict
