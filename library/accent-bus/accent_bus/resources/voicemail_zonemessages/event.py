# resources/voicemail_zonemessages/event.py
from typing import ClassVar

from accent_bus.resources.common.event import ServiceEvent


class VoicemailZoneMessagesEvent(ServiceEvent):
    """Base class for Voicemail Zone Messages events."""

    service: ClassVar[str] = "confd"
    content: dict = {}


class VoicemailZoneMessagesEditedEvent(VoicemailZoneMessagesEvent):
    """Event for when voicemail zone messages configuration is edited."""

    name: ClassVar[str] = "voicemail_zonemessages_edited"
    routing_key_fmt: ClassVar[str] = "config.voicemail_zonemessages.edited"
