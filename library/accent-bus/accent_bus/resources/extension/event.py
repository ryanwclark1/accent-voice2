# resources/extension/event.py
from typing import ClassVar

from resources.common.event import TenantEvent


class ExtensionEvent(TenantEvent):
    """Base class for Extension events."""

    service: ClassVar[str] = "confd"
    content: dict


class ExtensionCreatedEvent(ExtensionEvent):
    """Event for when an extension is created."""

    name: ClassVar[str] = "extension_created"
    routing_key_fmt: ClassVar[str] = "config.extensions.created"

    def __init__(
        self,
        extension_id: int,
        exten: str,
        context: str,
        **data,
    ):
        content = {
            "id": int(extension_id),
            "exten": exten,
            "context": context,
        }
        super().__init__(content=content, **data)


class ExtensionDeletedEvent(ExtensionEvent):
    """Event for when an extension is deleted."""

    name: ClassVar[str] = "extension_deleted"
    routing_key_fmt: ClassVar[str] = "config.extensions.deleted"

    def __init__(
        self,
        extension_id: int,
        exten: str,
        context: str,
        **data,
    ):
        content = {
            "id": int(extension_id),
            "exten": exten,
            "context": context,
        }
        super().__init__(content=content, **data)


class ExtensionEditedEvent(ExtensionEvent):
    """Event for when an extension is edited."""

    name: ClassVar[str] = "extension_edited"
    routing_key_fmt: ClassVar[str] = "config.extensions.edited"

    def __init__(
        self,
        extension_id: int,
        exten: str,
        context: str,
        **data,
    ):
        content = {
            "id": int(extension_id),
            "exten": exten,
            "context": context,
        }
        super().__init__(content=content, **data)
