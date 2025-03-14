# accent_bus/resources/plugins/types.py
# Copyright 2025 Accent Communications

"""Plugin types."""

from __future__ import annotations

from typing import Literal, TypedDict


class PluginErrorDict(TypedDict, total=False):
    """Dictionary representing a plugin error."""

    error_id: str
    message: str
    resource: Literal["plugins"]
    details: dict
