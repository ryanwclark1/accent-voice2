# resources/line_device/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent

from .types import DeviceDict, LineDict


class LineDeviceEvent(TenantEvent):
    """Base class for Line Device events."""

    service: ClassVar[str] = "confd"
    content: dict


class LineDeviceAssociatedEvent(LineDeviceEvent):
    """Event for when a device is associated with a line."""

    name: ClassVar[str] = "line_device_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.lines.{line[id]}.devices.{device[id]}.updated"
    )

    def __init__(
        self,
        line: LineDict,
        device: DeviceDict,
        **data,
    ):
        content = {"line": line, "device": device}
        super().__init__(content=content, **data)


class LineDeviceDissociatedEvent(LineDeviceEvent):
    """Event for when a device is dissociated from a line."""

    name: ClassVar[str] = "line_device_dissociated"
    routing_key_fmt: ClassVar[str] = (
        "config.lines.{line[id]}.devices.{device[id]}.deleted"
    )

    def __init__(self, line: LineDict, device: DeviceDict, **data):
        content = {"line": line, "device": device}
        super().__init__(content=content, **data)
