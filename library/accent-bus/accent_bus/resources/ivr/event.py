# accent_bus/resources/ivr/event.py
# Copyright 2025 Accent Communications

"""IVR events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class IVRCreatedEvent(TenantEvent):
    """Event for when an IVR is created."""

    service = "confd"
    name = "ivr_created"
    routing_key_fmt = "config.ivr.created"

    def __init__(self, ivr_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            ivr_id (int): The ID of the IVR.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {"id": ivr_id}
        super().__init__(content, tenant_uuid)


class IVRDeletedEvent(TenantEvent):
    """Event for when an IVR is deleted."""

    service = "confd"
    name = "ivr_deleted"
    routing_key_fmt = "config.ivr.deleted"

    def __init__(self, ivr_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
          ivr_id: IVR ID
          tenant_uuid: tenant UUID

        """
        content = {"id": ivr_id}
        super().__init__(content, tenant_uuid)


class IVREditedEvent(TenantEvent):
    """Event for when an IVR is edited."""

    service = "confd"
    name = "ivr_edited"
    routing_key_fmt = "config.ivr.edited"

    def __init__(self, ivr_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           ivr_id: IVR ID
           tenant_uuid: tenant UUID

        """
        content = {"id": ivr_id}
        super().__init__(content, tenant_uuid)
