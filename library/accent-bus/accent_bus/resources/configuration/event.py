# accent_bus/resources/configuration/event.py
# Copyright 2025 Accent Communications

"""Configuration events."""

from accent_bus.resources.common.event import ServiceEvent


class LiveReloadEditedEvent(ServiceEvent):
    """Event for when live reload configuration is edited."""

    service = "confd"
    name = "live_reload_edited"
    routing_key_fmt = "config.live_reload.edited"

    def __init__(self, live_reload_enabled: bool) -> None:
        """Initialize the event.

        Args:
          live_reload_enabled: Live Reload Enabled.

        """
        content = {"live_reload_enabled": live_reload_enabled}
        super().__init__(content)
