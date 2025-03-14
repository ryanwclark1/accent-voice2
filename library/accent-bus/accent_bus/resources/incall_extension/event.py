# accent_bus/resources/incall_extension/event.py
# Copyright 2025 Accent Communications

"""Incall extension events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class IncallExtensionAssociatedEvent(TenantEvent):
    """Event for when an incall extension is associated."""

    service = "confd"
    name = "incall_extension_associated"
    routing_key_fmt = "config.incalls.extensions.updated"

    def __init__(
        self,
        incall_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
            incall_id (int): The ID of the incall.
            extension_id (int): The ID of the extension.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {
            "incall_id": incall_id,
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)


class IncallExtensionDissociatedEvent(TenantEvent):
    """Event for when an incall extension is dissociated."""

    service = "confd"
    name = "incall_extension_dissociated"
    routing_key_fmt = "config.incalls.extensions.deleted"

    def __init__(
        self,
        incall_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            incall_id: Incall ID
            extension_id: Extension ID
            tenant_uuid: tenant UUID

        """
        content = {
            "incall_id": incall_id,
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)
