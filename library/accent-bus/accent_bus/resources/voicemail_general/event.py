# accent_bus/resources/voicemail_general/event.py
# Copyright 2025 Accent Communications

"""Voicemail general events."""

from accent_bus.resources.common.event import ServiceEvent


class VoicemailGeneralEditedEvent(ServiceEvent):
    """Event for when general voicemail settings are edited."""

    service = "confd"
    name = "voicemail_general_edited"
    routing_key_fmt = "config.voicemail_general.edited"

    def __init__(self) -> None:
        """Initialize the event."""
        super().__init__()
