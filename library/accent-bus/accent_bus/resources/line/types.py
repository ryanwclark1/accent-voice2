# accent_bus/resources/line/types.py
# Copyright 2025 Accent Communications

"""Line types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class LineDict(TypedDict, total=False):
    """Dictionary representing a line."""

    id: int
    protocol: str
    name: str
    tenant_uuid: UUIDStr
