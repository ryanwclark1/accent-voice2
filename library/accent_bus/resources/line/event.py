# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import LineDict


class LineCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_created'
    routing_key_fmt = 'config.line.created'

    def __init__(self, line: LineDict, tenant_uuid: UUIDStr):
        super().__init__(line, tenant_uuid)


class LineDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'line_deleted'
    routing_key_fmt = 'config.line.deleted'

    def __init__(self, line: LineDict, tenant_uuid: UUIDStr):
        super().__init__(line, tenant_uuid)


class LineEditedEvent(TenantEvent):
    service = 'confd'
    name = 'line_edited'
    routing_key_fmt = 'config.line.edited'

    def __init__(self, line: LineDict, tenant_uuid: UUIDStr):
        super().__init__(line, tenant_uuid)


class LineStatusUpdatedEvent(TenantEvent):
    service = 'calld'
    name = 'line_status_updated'
    routing_key_fmt = 'lines.{id}.status.updated'

    def __init__(
        self,
        line_id: int,
        technology: str,
        endpoint_name: str,
        endpoint_registered: bool,
        endpoint_current_call_count: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'id': line_id,
            'technology': technology,
            'name': endpoint_name,
            'registered': endpoint_registered,
            'current_call_count': endpoint_current_call_count,
        }
        super().__init__(content, tenant_uuid)
