# resources/line_extension/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class LineExtensionEvent(TenantEvent):
    """Base class for Line Extension events."""

    service: ClassVar[str] = "confd"
    content: dict


class LineExtensionAssociatedEvent(LineExtensionEvent):
    """Event for when an extension is associated with a line."""

    name: ClassVar[str] = "line_extension_associated"
    routing_key_fmt: ClassVar[str] = "config.line_extension_associated.updated"

    def __init__(
        self,
        line_id: int,
        extension_id: int,
        **data,
    ):
        content = {"line_id": line_id, "extension_id": extension_id}
        super().__init__(content=content, **data)


class LineExtensionDissociatedEvent(LineExtensionEvent):
    """Event for when an extension is dissociated from a line."""

    name: ClassVar[str] = "line_extension_dissociated"
    routing_key_fmt: ClassVar[str] = "config.line_extension_associated.deleted"

    def __init__(
        self,
        line_id: int,
        extension_id: int,
        **data,
    ):
        content = {"line_id": line_id, "extension_id": extension_id}
        super().__init__(content=content, **data)
