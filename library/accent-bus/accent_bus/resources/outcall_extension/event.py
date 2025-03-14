# accent_bus/resources/outcall_extension/event.py
# Copyright 2025 Accent Communications

"""Outcall extension events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class OutcallExtensionAssociatedEvent(TenantEvent):
    """Event for when an outcall extension is associated."""

    service = "confd"
    name = "outcall_extension_associated"
    routing_key_fmt = "config.outcalls.extensions.updated"

    def __init__(
        self,
        outcall_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           outcall_id: Outcall ID
           extension_id: Extension ID
           tenant_uuid: tenant UUID

        """
        content = {
            "outcall_id": outcall_id,
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)


class OutcallExtensionDissociatedEvent(TenantEvent):
    """Event for when an outcall extension is dissociated."""

    service = "confd"
    name = "outcall_extension_dissociated"
    routing_key_fmt = "config.outcalls.extensions.deleted"

    def __init__(
        self,
        outcall_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
           outcall_id: Outcall ID
           extension_id: Extension ID
           tenant_uuid: tenant UUID

        """
        content = {
            "outcall_id": outcall_id,
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)
