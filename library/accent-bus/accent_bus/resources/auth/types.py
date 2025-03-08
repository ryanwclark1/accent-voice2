# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class TenantDict(TypedDict, total=False):
    uuid: UUIDStr
    name: str
    slug: str
    domain_names: list[str]
