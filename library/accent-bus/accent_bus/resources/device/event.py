# resources/device/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class DeviceEvent(TenantEvent):
    """Base class for Device events."""

    service: ClassVar[str] = "confd"
    content: dict


class DeviceCreatedEvent(DeviceEvent):
    """Event for when a device is created."""

    name: ClassVar[str] = "device_created"
    routing_key_fmt: ClassVar[str] = "config.device.created"

    def __init__(self, device_id: str, **data):
        content = {"id": device_id}
        super().__init__(content=content, **data)


class DeviceDeletedEvent(DeviceEvent):
    """Event for when a device is deleted."""

    name: ClassVar[str] = "device_deleted"
    routing_key_fmt: ClassVar[str] = "config.device.deleted"

    def __init__(self, device_id: str, **data):
        content = {"id": device_id}
        super().__init__(content=content, **data)


class DeviceEditedEvent(DeviceEvent):
    """Event for when a device is edited."""

    name: ClassVar[str] = "device_edited"
    routing_key_fmt: ClassVar[str] = "config.device.edited"

    def __init__(self, device_id: str, **data):
        content = {"id": device_id}
        super().__init__(content=content, **data)
