# accent_bus/resources/confbridge/event.py
# Copyright 2025 Accent Communications

"""Confbridge events."""

from accent_bus.resources.common.event import ServiceEvent


class ConfBridgeAccentDefaultBridgeEditedEvent(ServiceEvent):
    """Event for when the default confbridge bridge is edited."""

    service = "confd"
    name = "confbridge_accent_default_bridge_edited"
    routing_key_fmt = "config.confbridge_accent_default_bridge.edited"

    def __init__(self) -> None:
        """Initialize event."""
        super().__init__()


class ConfBridgeAccentDefaultUserEditedEvent(ServiceEvent):
    """Event for when the default confbridge user is edited."""

    service = "confd"
    name = "confbridge_accent_default_user_edited"
    routing_key_fmt = "config.confbridge_accent_default_user.edited"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
