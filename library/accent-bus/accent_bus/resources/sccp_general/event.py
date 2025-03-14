# resources/sccp_general/event.py
from typing import ClassVar

from resources.common.event import ServiceEvent


class SCCPGeneralEvent(ServiceEvent):
    """Base class for general SCCP configuration events."""

    service: ClassVar[str] = "confd"
    content: dict = {}


class SCCPGeneralEditedEvent(SCCPGeneralEvent):
    """Event for when the general SCCP configuration is edited."""

    name: ClassVar[str] = "sccp_general_edited"
    routing_key_fmt: ClassVar[str] = "config.sccp_general.edited"
