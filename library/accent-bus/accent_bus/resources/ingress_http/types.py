# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class IngressHTTPDict(TypedDict, total=False):
    uuid: UUIDStr
    tenant_uuid: UUIDStr
    uri: str
