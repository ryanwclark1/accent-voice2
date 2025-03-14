# resources/localization/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent

from .types import LocalizationDict


class LocalizationEvent(TenantEvent):
    """Base class for Localization events."""

    service: ClassVar[str] = "confd"
    content: dict


class LocalizationEditedEvent(LocalizationEvent):
    """Event for when localization settings are edited."""

    name: ClassVar[str] = "localization_edited"
    routing_key_fmt: ClassVar[str] = "config.localization.edited"

    def __init__(self, localization: LocalizationDict, **data):
        super().__init__(content=localization.model_dump(), **data)
