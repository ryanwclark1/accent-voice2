# resources/conference_extension/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class ConferenceExtensionEvent(TenantEvent):
    """Base class for Conference Extension events."""

    service: ClassVar[str] = "confd"
    content: dict


class ConferenceExtensionAssociatedEvent(ConferenceExtensionEvent):
    """Event for when a conference extension is associated."""

    name: ClassVar[str] = "conference_extension_associated"
    routing_key_fmt: ClassVar[str] = "config.conferences.extensions.updated"

    def __init__(self, conference_id: int, extension_id: int, **data):
        content = {
            "conference_id": conference_id,
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)


class ConferenceExtensionDissociatedEvent(ConferenceExtensionEvent):
    """Event for when a conference extension is dissociated."""

    name: ClassVar[str] = "conference_extension_dissociated"
    routing_key_fmt: ClassVar[str] = "config.conferences.extensions.deleted"

    def __init__(self, conference_id: int, extension_id: int, **data):
        content = {
            "conference_id": conference_id,
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)
