# Copyright 2025 Accent Communications

"""Data models for the Accent Market client.

This module contains Pydantic models for structured data handling in the
Accent Market API client.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PluginResponse(BaseModel):
    """Response model for plugin data.

    Attributes:
        id: Unique identifier for the plugin
        name: Name of the plugin
        version: Version string
        description: Plugin description
        enabled: Whether the plugin is enabled
        metadata: Additional plugin metadata

    """

    id: str
    name: str
    version: str
    description: str | None = None
    enabled: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class PluginListResponse(BaseModel):
    """Response model for a list of plugins.

    Attributes:
        plugins: List of plugin objects
        total: Total number of plugins

    """

    plugins: list[PluginResponse]
    total: int
