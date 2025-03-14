# resources/confbridge/event.py
from typing import ClassVar

from resources.common.event import ServiceEvent


class ConfBridgeEvent(ServiceEvent):
    """Base class for confbridge events."""

    service: ClassVar[str] = "confd"
    content: dict = {}  # All service events should define content.


class ConfBridgeAccentDefaultBridgeEditedEvent(ConfBridgeEvent):
    """Event for when the default confbridge bridge is edited."""

    name: ClassVar[str] = "confbridge_accent_default_bridge_edited"
    routing_key_fmt: ClassVar[str] = "config.confbridge_accent_default_bridge.edited"


class ConfBridgeAccentDefaultUserEditedEvent(ConfBridgeEvent):
    """Event for when the default confbridge user is edited."""

    name: ClassVar[str] = "confbridge_accent_default_user_edited"
    routing_key_fmt: ClassVar[str] = "config.confbridge_accent_default_user.edited"
