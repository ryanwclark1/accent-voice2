# accent_bus/resources/line_device/event.py
# Copyright 2025 Accent Communications

"""Line device events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import DeviceDict, LineDict


class LineDeviceAssociatedEvent(TenantEvent):
    """Event for when a line device is associated."""

    service = "confd"
    name = "line_device_associated"
    routing_key_fmt = "config.lines.{line[id]}.devices.{device[id]}.updated"

    def __init__(
        self,
        line: LineDict,
        device: DeviceDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           line: Line
           device: Device
           tenant_uuid: tenant UUID

        """
        content = {"line": line, "device": device}
        super().__init__(content, tenant_uuid)


class LineDeviceDissociatedEvent(TenantEvent):
    """Event for when a line device is dissociated."""

    service = "confd"
    name = "line_device_dissociated"
    routing_key_fmt = "config.lines.{line[id]}.devices.{device[id]}.deleted"

    def __init__(
        self,
        line: LineDict,
        device: DeviceDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           line: Line
           device: Device
           tenant_uuid: tenant UUID

        """
        content = {"line": line, "device": device}
        super().__init__(content, tenant_uuid)
