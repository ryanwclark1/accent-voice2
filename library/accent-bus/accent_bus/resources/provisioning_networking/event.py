# accent_bus/resources/provisioning_networking/event.py
# Copyright 2025 Accent Communications

"""Provisioning networking events."""

from accent_bus.resources.common.event import ServiceEvent


class ProvisioningNetworkingEditedEvent(ServiceEvent):
    """Event for when provisioning networking configuration is edited."""

    service = "confd"
    name = "provisioning_networking_edited"
    routing_key_fmt = "config.provisioning.networking.edited"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
