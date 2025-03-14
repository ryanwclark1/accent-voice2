# accent_bus/resources/auth/types.py
# Copyright 2025 Accent Communications

"""Auth types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class TenantDict(TypedDict, total=False):
    """Dictionary representing a tenant."""

    uuid: UUIDStr
    name: str
    slug: str
    domain_names: list[str]
