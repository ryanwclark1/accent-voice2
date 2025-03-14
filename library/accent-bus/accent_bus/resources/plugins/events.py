# accent_bus/resources/plugins/events.py
# Copyright 2025 Accent Communications

"""Plugin events."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_bus.resources.common.event import ServiceEvent

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr

    from .types import PluginErrorDict


class PluginInstallProgressEvent(ServiceEvent):
    """Event for plugin installation progress."""

    service = "plugind"
    name = "plugin_install_progress"
    routing_key_fmt = "plugin.install.{uuid}.{status}"

    def __init__(
        self,
        plugin_uuid: UUIDStr,
        status: str,
        errors: PluginErrorDict | None = None,
    ) -> None:
        """Initialize the event.

        Args:
            plugin_uuid (UUIDStr): plugin UUID.
            status (str): Installation status.
            errors (PluginErrorDict | None): Optional error details.

        """
        content = {"uuid": plugin_uuid, "status": status}
        if errors:
            content.update(errors=errors)  # type: ignore[call-overload]
        super().__init__(content)


class PluginUninstallProgressEvent(ServiceEvent):
    """Event for plugin uninstallation progress."""

    service = "plugind"
    name = "plugin_uninstall_progress"
    routing_key_fmt = "plugin.uninstall.{uuid}.{status}"

    def __init__(
        self,
        plugin_uuid: UUIDStr,
        status: str,
        errors: PluginErrorDict | None = None,
    ) -> None:
        """Initialize event.

        Args:
            plugin_uuid (UUIDStr): plugin UUID.
            status (str):  uninstallation status.
            errors (PluginErrorDict | None): Optional error details.

        """
        content = {"uuid": plugin_uuid, "status": status}
        if errors:
            content.update(errors=errors)  # type: ignore[call-overload]
        super().__init__(content)
