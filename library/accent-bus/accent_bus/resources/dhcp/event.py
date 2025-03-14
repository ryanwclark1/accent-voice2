# resources/dhcp/event.py
from typing import ClassVar

from resources.common.event import ServiceEvent


class DHCPEvent(ServiceEvent):
    """Base class for DHCP events."""

    service: ClassVar[str] = "confd"
    content: dict = {}  # ServiceEvents should have a content attribute.


class DHCPEditedEvent(DHCPEvent):
    """Event for when DHCP configuration is edited."""

    name: ClassVar[str] = "dhcp_edited"
    routing_key_fmt: ClassVar[str] = "config.dhcp.edited"
