# accent_bus/resources/context/types.py
# Copyright 2025 Accent Communications

"""Context types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class ContextDict(TypedDict, total=False):
    """Dictionary representing a context."""

    id: int
    name: str
    type: str
    tenant_uuid: UUIDStr
