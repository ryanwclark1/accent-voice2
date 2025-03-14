# resources/provisioning_networking/event.py
from typing import ClassVar

from accent_bus.resources.common.event import ServiceEvent


class ProvisioningNetworkingEvent(ServiceEvent):
    """Base class for Provisioning Networking events."""

    service: ClassVar[str] = "confd"
    content: dict = {}  # ServiceEvents should define 'content'


class ProvisioningNetworkingEditedEvent(ProvisioningNetworkingEvent):
    """Event for when provisioning networking configuration is edited."""

    name: ClassVar[str] = "provisioning_networking_edited"
    routing_key_fmt: ClassVar[str] = "config.provisioning.networking.edited"
