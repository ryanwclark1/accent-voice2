# resources/iax_callnumberlimits/event.py
from typing import ClassVar

from resources.common.event import ServiceEvent


class IAXCallNumberLimitsEvent(ServiceEvent):
    """Base class for IAX Call Number Limits events."""

    service: ClassVar[str] = "confd"
    content: dict = {}


class IAXCallNumberLimitsEditedEvent(IAXCallNumberLimitsEvent):
    """Event for when IAX call number limits are edited."""

    name: ClassVar[str] = "iax_callnumberlimits_edited"
    routing_key_fmt: ClassVar[str] = "config.iax_callnumberlimits.edited"
