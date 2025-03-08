# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class OutcallTrunksAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_trunks_associated'
    routing_key_fmt = 'config.outcalls.trunks.updated'

    def __init__(
        self,
        outcall_id: int,
        trunk_ids: list[int],
        tenant_uuid: UUIDStr,
    ):
        content = {
            'outcall_id': outcall_id,
            'trunk_ids': trunk_ids,
        }
        super().__init__(content, tenant_uuid)
