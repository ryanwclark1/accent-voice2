# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class DeviceCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'device_created'
    routing_key_fmt = 'config.device.created'

    def __init__(self, device_id: str, tenant_uuid: UUIDStr):
        content = {'id': device_id}
        super().__init__(content, tenant_uuid)


class DeviceDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'device_deleted'
    routing_key_fmt = 'config.device.deleted'

    def __init__(self, device_id: str, tenant_uuid: UUIDStr):
        content = {'id': device_id}
        super().__init__(content, tenant_uuid)


class DeviceEditedEvent(TenantEvent):
    service = 'confd'
    name = 'device_edited'
    routing_key_fmt = 'config.device.edited'

    def __init__(self, device_id: str, tenant_uuid: UUIDStr):
        content = {'id': device_id}
        super().__init__(content, tenant_uuid)
