# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class ContextDict(TypedDict, total=False):
    id: int
    name: str
    type: str
    tenant_uuid: UUIDStr
