# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class ContextContextsAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'contexts_associated'
    routing_key_fmt = 'config.contexts.contexts.updated'

    def __init__(
        self,
        context_id: int,
        context_ids: list[int],
        tenant_uuid: UUIDStr,
    ):
        content = {
            'context_id': context_id,
            'context_ids': context_ids,
        }
        super().__init__(content, tenant_uuid)
