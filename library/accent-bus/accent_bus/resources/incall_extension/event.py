# resources/incall_extension/event.py
from typing import ClassVar

from resources.common.event import TenantEvent


class IncallExtensionEvent(TenantEvent):
    """Base class for Incall Extension events."""

    service: ClassVar[str] = "confd"
    content: dict


class IncallExtensionAssociatedEvent(IncallExtensionEvent):
    """Event for when an extension is associated with an incall."""

    name: ClassVar[str] = "incall_extension_associated"
    routing_key_fmt: ClassVar[str] = "config.incalls.extensions.updated"

    def __init__(self, incall_id: int, extension_id: int, **data):
        content = {
            "incall_id": incall_id,
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)


class IncallExtensionDissociatedEvent(IncallExtensionEvent):
    """Event for when an extension is dissociated from an incall."""

    name: ClassVar[str] = "incall_extension_dissociated"
    routing_key_fmt: ClassVar[str] = "config.incalls.extensions.deleted"

    def __init__(self, incall_id: int, extension_id: int, **data):
        content = {
            "incall_id": incall_id,
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)
