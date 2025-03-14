# resources/configuration/event.py
from typing import ClassVar

from resources.common.event import ServiceEvent


class ConfigurationEvent(ServiceEvent):
    """Base class for configuration events."""

    service: ClassVar[str] = "confd"
    content: dict


class LiveReloadEditedEvent(ConfigurationEvent):
    """Event for when live reload configuration is edited."""

    name: ClassVar[str] = "live_reload_edited"
    routing_key_fmt: ClassVar[str] = "config.live_reload.edited"

    def __init__(self, live_reload_enabled: bool):
        content = {"live_reload_enabled": live_reload_enabled}
        super().__init__(content=content)
