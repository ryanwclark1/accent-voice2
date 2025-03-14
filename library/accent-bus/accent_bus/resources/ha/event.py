# resources/ha/event.py
from typing import ClassVar

from accent_bus.resources.common.event import ServiceEvent


class HAEvent(ServiceEvent):
    """Base class for HA (High Availability) events."""

    service: ClassVar[str] = "confd"
    content: dict = {}  # All ServiceEvents must define 'content'.


class HAEditedEvent(HAEvent):
    """Event for when HA configuration is edited."""

    name: ClassVar[str] = "ha_edited"
    routing_key_fmt: ClassVar[str] = "config.ha.edited"
