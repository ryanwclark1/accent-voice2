# resources/iax_general/event.py
from typing import ClassVar

from accent_bus.resources.common.event import ServiceEvent


class IAXGeneralEvent(ServiceEvent):
    """Base class for IAX General events."""

    service: ClassVar[str] = "confd"
    content: dict = {}


class IAXGeneralEditedEvent(IAXGeneralEvent):
    """Event for when general IAX configuration is edited."""

    name: ClassVar[str] = "iax_general_edited"
    routing_key_fmt: ClassVar[str] = "config.iax_general.edited"
