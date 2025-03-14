# accent_bus/resources/hep/event.py
# Copyright 2025 Accent Communications

"""HEP events."""

from accent_bus.resources.common.event import ServiceEvent


class HEPGeneralEditedEvent(ServiceEvent):
    """Event for when general HEP settings are edited."""

    service = "confd"
    name = "hep_general_edited"
    routing_key_fmt = "config.hep_general.edited"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
