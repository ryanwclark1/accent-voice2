# accent_bus/resources/dhcp/event.py
# Copyright 2025 Accent Communications

"""DHCP events."""

from accent_bus.resources.common.event import ServiceEvent


class DHCPEditedEvent(ServiceEvent):
    """Event for when DHCP configuration is edited."""

    service = "confd"
    name = "dhcp_edited"
    routing_key_fmt = "config.dhcp.edited"

    def __init__(self) -> None:
        """Initialize event."""
        super().__init__()
