# accent_bus/resources/group/types.py
# Copyright 2025 Accent Communications

"""Group types."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class GroupDict(TypedDict, total=False):
    """Dictionary representing a group."""

    id: int
    uuid: UUIDStr
