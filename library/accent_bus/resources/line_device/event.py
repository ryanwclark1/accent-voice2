# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import DeviceDict, LineDict


class LineDeviceAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_device_associated'
    routing_key_fmt = 'config.lines.{line[id]}.devices.{device[id]}.updated'

    def __init__(
        self,
        line: LineDict,
        device: DeviceDict,
        tenant_uuid: UUIDStr,
    ):
        content = {'line': line, 'device': device}
        super().__init__(content, tenant_uuid)


class LineDeviceDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_device_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.devices.{device[id]}.deleted'

    def __init__(
        self,
        line: LineDict,
        device: DeviceDict,
        tenant_uuid: UUIDStr,
    ):
        content = {'line': line, 'device': device}
        super().__init__(content, tenant_uuid)
