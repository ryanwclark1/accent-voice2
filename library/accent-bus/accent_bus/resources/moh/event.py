# accent_bus/resources/moh/event.py
# Copyright 2025 Accent Communications

"""MOH events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import MOHDict


class MOHCreatedEvent(TenantEvent):
    """Event for when a MOH is created."""

    service = "confd"
    name = "moh_created"
    routing_key_fmt = "config.moh.created"

    def __init__(self, moh: MOHDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           moh: MOH
           tenant_uuid: tenant UUID

        """
        super().__init__(moh, tenant_uuid)


class MOHDeletedEvent(TenantEvent):
    """Event for when a MOH is deleted."""

    service = "confd"
    name = "moh_deleted"
    routing_key_fmt = "config.moh.deleted"

    def __init__(self, moh: MOHDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            moh (MOHDict): The MOH details.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(moh, tenant_uuid)


class MOHEditedEvent(TenantEvent):
    """Event for when a MOH is edited."""

    service = "confd"
    name = "moh_edited"
    routing_key_fmt = "config.moh.edited"

    def __init__(self, moh: MOHDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
          moh: MOH
          tenant_uuid: tenant UUID

        """
        super().__init__(moh, tenant_uuid)
