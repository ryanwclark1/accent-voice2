# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class OutcallCallPermissionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_call_permission_associated'
    routing_key_fmt = 'config.outcalls.{outcall_id}.callpermissions.updated'

    def __init__(
        self,
        outcall_id: int,
        call_permission_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'outcall_id': outcall_id,
            'call_permission_id': call_permission_id,
        }
        super().__init__(content, tenant_uuid)


class OutcallCallPermissionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_call_permission_dissociated'
    routing_key_fmt = 'config.outcalls.{outcall_id}.callpermissions.deleted'

    def __init__(
        self,
        outcall_id: int,
        call_permission_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'outcall_id': outcall_id,
            'call_permission_id': call_permission_id,
        }
        super().__init__(content, tenant_uuid)
