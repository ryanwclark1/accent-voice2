# resources/voicemail_general/event.py
from typing import ClassVar

from accent_bus.resources.common.event import ServiceEvent


class VoicemailGeneralEvent(ServiceEvent):
    """Base class for general Voicemail events."""

    service: ClassVar[str] = "confd"
    content: dict = {}


class VoicemailGeneralEditedEvent(VoicemailGeneralEvent):
    """Event for when the general voicemail configuration is edited."""

    name: ClassVar[str] = "voicemail_general_edited"
    routing_key_fmt: ClassVar[str] = "config.voicemail_general.edited"
