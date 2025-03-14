# accent_bus/resources/sccp_general/event.py
# Copyright 2025 Accent Communications

"""SCCP general events."""

from accent_bus.resources.common.event import ServiceEvent


class SCCPGeneralEditedEvent(ServiceEvent):
    """Event for when general SCCP settings are edited."""

    service = "confd"
    name = "sccp_general_edited"
    routing_key_fmt = "config.sccp_general.edited"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
