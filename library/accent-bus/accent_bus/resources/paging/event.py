# accent_bus/resources/paging/event.py
# Copyright 2025 Accent Communications

"""Paging events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class PagingCreatedEvent(TenantEvent):
    """Event for when a paging is created."""

    service = "confd"
    name = "paging_created"
    routing_key_fmt = "config.pagings.created"

    def __init__(self, paging_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            paging_id (int): The ID of the paging.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {"id": paging_id}
        super().__init__(content, tenant_uuid)


class PagingDeletedEvent(TenantEvent):
    """Event for when a paging is deleted."""

    service = "confd"
    name = "paging_deleted"
    routing_key_fmt = "config.pagings.deleted"

    def __init__(self, paging_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            paging_id (int): The ID of the paging.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {"id": paging_id}
        super().__init__(content, tenant_uuid)


class PagingEditedEvent(TenantEvent):
    """Event for when a paging is edited."""

    service = "confd"
    name = "paging_edited"
    routing_key_fmt = "config.pagings.edited"

    def __init__(self, paging_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           paging_id: Paging ID
           tenant_uuid: tenant UUID

        """
        content = {"id": paging_id}
        super().__init__(content, tenant_uuid)
