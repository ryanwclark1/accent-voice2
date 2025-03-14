# resources/sip_general/event.py
from typing import ClassVar

from resources.common.event import ServiceEvent


class SIPGeneralEvent(ServiceEvent):
    """Base class for general SIP configuration events."""

    service: ClassVar[str] = "confd"
    content: dict = {}


class SIPGeneralEditedEvent(SIPGeneralEvent):
    """Event for when the general SIP configuration is edited."""

    name: ClassVar[str] = "sip_general_edited"
    routing_key_fmt: ClassVar[str] = "config.sip_general.edited"
