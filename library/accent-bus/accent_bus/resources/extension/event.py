# accent_bus/resources/extension/event.py
# Copyright 2025 Accent Communications

"""Extension events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class ExtensionCreatedEvent(TenantEvent):
    """Event for when an extension is created."""

    service = "confd"
    name = "extension_created"
    routing_key_fmt = "config.extensions.created"

    def __init__(
        self,
        extension_id: int,
        exten: str,
        context: str,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           extension_id: Extension ID
           exten: Extension number
           context: Context
           tenant_uuid: tenant UUID

        """
        content = {
            "id": int(extension_id),
            "exten": exten,
            "context": context,
        }
        super().__init__(content, tenant_uuid)


class ExtensionDeletedEvent(TenantEvent):
    """Event for when an extension is deleted."""

    service = "confd"
    name = "extension_deleted"
    routing_key_fmt = "config.extensions.deleted"

    def __init__(
        self,
        extension_id: int,
        exten: str,
        context: str,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            extension_id (int): Extension ID.
            exten (str): Extension.
            context (str): Context.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {
            "id": int(extension_id),
            "exten": exten,
            "context": context,
        }
        super().__init__(content, tenant_uuid)


class ExtensionEditedEvent(TenantEvent):
    """Event for when an extension is edited."""

    service = "confd"
    name = "extension_edited"
    routing_key_fmt = "config.extensions.edited"

    def __init__(
        self,
        extension_id: int,
        exten: str,
        context: str,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           extension_id: Extension ID
           exten: Extension Number
           context: Context
           tenant_uuid: tenant UUID

        """
        content = {
            "id": int(extension_id),
            "exten": exten,
            "context": context,
        }
        super().__init__(content, tenant_uuid)
