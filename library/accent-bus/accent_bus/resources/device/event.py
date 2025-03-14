# accent_bus/resources/device/event.py
# Copyright 2025 Accent Communications

"""Device events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class DeviceCreatedEvent(TenantEvent):
    """Event for when a device is created."""

    service = "confd"
    name = "device_created"
    routing_key_fmt = "config.device.created"

    def __init__(self, device_id: str, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
           device_id: Device ID
           tenant_uuid: tenant UUID

        """
        content = {"id": device_id}
        super().__init__(content, tenant_uuid)


class DeviceDeletedEvent(TenantEvent):
    """Event for when a device is deleted."""

    service = "confd"
    name = "device_deleted"
    routing_key_fmt = "config.device.deleted"

    def __init__(self, device_id: str, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            device_id (str):  device ID.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        content = {"id": device_id}
        super().__init__(content, tenant_uuid)


class DeviceEditedEvent(TenantEvent):
    """Event for when a device is edited."""

    service = "confd"
    name = "device_edited"
    routing_key_fmt = "config.device.edited"

    def __init__(self, device_id: str, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
          device_id: Device ID
          tenant_uuid: tenant UUID

        """
        content = {"id": device_id}
        super().__init__(content, tenant_uuid)
