# accent_bus/resources/moh/types.py
# Copyright 2025 Accent Communications

"""MOH types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class MOHDict(TypedDict, total=False):
    """Dictionary representing MOH."""

    uuid: UUIDStr
    tenant_uuid: UUIDStr
    name: str
