# accent_bus/resources/ha/event.py
# Copyright 2025 Accent Communications

"""HA events."""

from accent_bus.resources.common.event import ServiceEvent


class HAEditedEvent(ServiceEvent):
    """Event for when HA configuration is edited."""

    service = "confd"
    name = "ha_edited"
    routing_key_fmt = "config.ha.edited"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
