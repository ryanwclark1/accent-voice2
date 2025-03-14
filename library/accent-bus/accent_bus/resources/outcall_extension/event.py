# resources/outcall_extension/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class OutcallExtensionEvent(TenantEvent):
    """Base class for Outcall Extension events."""

    service: ClassVar[str] = "confd"
    content: dict


class OutcallExtensionAssociatedEvent(OutcallExtensionEvent):
    """Event for when an extension is associated with an outcall."""

    name: ClassVar[str] = "outcall_extension_associated"
    routing_key_fmt: ClassVar[str] = "config.outcalls.extensions.updated"

    def __init__(
        self,
        outcall_id: int,
        extension_id: int,
        **data,
    ):
        content = {
            "outcall_id": outcall_id,
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)


class OutcallExtensionDissociatedEvent(OutcallExtensionEvent):
    """Event for when an extension is dissociated from an outcall."""

    name: ClassVar[str] = "outcall_extension_dissociated"
    routing_key_fmt: ClassVar[str] = "config.outcalls.extensions.deleted"

    def __init__(
        self,
        outcall_id: int,
        extension_id: int,
        **data,
    ):
        content = {
            "outcall_id": outcall_id,
            "extension_id": extension_id,
        }
        super().__init__(content=content, **data)
