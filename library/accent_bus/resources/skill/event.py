# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class SkillCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_created'
    routing_key_fmt = 'config.agents.skills.created'

    def __init__(self, skill_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(skill_id)}
        super().__init__(content, tenant_uuid)


class SkillDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_deleted'
    routing_key_fmt = 'config.agents.skills.deleted'

    def __init__(self, skill_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(skill_id)}
        super().__init__(content, tenant_uuid)


class SkillEditedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_edited'
    routing_key_fmt = 'config.agents.skills.edited'

    def __init__(self, skill_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(skill_id)}
        super().__init__(content, tenant_uuid)
