# resources/hep/event.py
from typing import ClassVar

from resources.common.event import ServiceEvent


class HEPEvent(ServiceEvent):
    """Base class for HEP (Homer Encapsulation Protocol) events."""

    service: ClassVar[str] = "confd"
    content: dict = {}  # ServiceEvents must define content


class HEPGeneralEditedEvent(HEPEvent):
    """Event for when general HEP configuration is edited."""

    name: ClassVar[str] = "hep_general_edited"
    routing_key_fmt: ClassVar[str] = "config.hep_general.edited"
