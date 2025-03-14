# accent_bus/resources/group_member/types.py
# Copyright 2025 Accent Communications

"""Group member types."""

from __future__ import annotations

from typing import TypedDict


class GroupExtensionDict(TypedDict, total=False):
    """Dictionary representing a group extension."""

    exten: str
    context: str
