# accent_bus/resources/sip_general/event.py
# Copyright 2025 Accent Communications

"""SIP general events."""

from accent_bus.resources.common.event import ServiceEvent


class SIPGeneralEditedEvent(ServiceEvent):
    """Event for when general SIP settings are edited."""

    service = "confd"
    name = "sip_general_edited"
    routing_key_fmt = "config.sip_general.edited"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
