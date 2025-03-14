# accent_bus/resources/voicemail_zonemessages/event.py
# Copyright 2025 Accent Communications

"""Voicemail zone messages events."""

from accent_bus.resources.common.event import ServiceEvent


class VoicemailZoneMessagesEditedEvent(ServiceEvent):
    """Event for when voicemail zone messages are edited."""

    service = "confd"
    name = "voicemail_zonemessages_edited"
    routing_key_fmt = "config.voicemail_zonemessages.edited"

    def __init__(self) -> None:
        """Initialize event."""
        super().__init__()
