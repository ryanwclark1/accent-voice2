# Copyright 2025 Accent Communications

"""Data models for the Accent Plugin Daemon client.

This module provides Pydantic models for structured data handling
in the Plugin Daemon API interactions.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PluginData(BaseModel):
    """Model representing a plugin.

    Attributes:
        name: Name of the plugin
        namespace: Namespace of the plugin
        version: Version of the plugin
        description: Description of the plugin
        enabled: Whether the plugin is enabled
        settings: Plugin settings

    """

    name: str
    namespace: str
    version: str
    description: str = ""
    enabled: bool = True
    settings: dict[str, Any] = Field(default_factory=dict)


class MarketData(BaseModel):
    """Model representing a marketplace entry.

    Attributes:
        name: Name of the plugin in the marketplace
        namespace: Namespace of the plugin
        version: Version of the plugin
        description: Description of the plugin
        author: Author of the plugin
        install_methods: Available installation methods

    """

    name: str
    namespace: str
    version: str
    description: str = ""
    author: str = ""
    install_methods: list[str] = Field(default_factory=list)


class ConfigData(BaseModel):
    """Model representing the plugin daemon configuration.

    Attributes:
        repositories: List of plugin repositories
        settings: Global plugin daemon settings

    """

    repositories: list[str] = Field(default_factory=list)
    settings: dict[str, Any] = Field(default_factory=dict)


class StatusData(BaseModel):
    """Model representing the plugin daemon status.

    Attributes:
        status: Current status of the plugin daemon
        version: Version of the plugin daemon
        uptime: Uptime in seconds
        plugins_loaded: Number of loaded plugins

    """

    status: str
    version: str
    uptime: float
    plugins_loaded: int
