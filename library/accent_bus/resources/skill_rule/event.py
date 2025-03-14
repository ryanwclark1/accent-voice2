# Copyright 2023 Accent Communications

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class SkillRuleCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_rule_created'
    routing_key_fmt = 'config.queues.skillrules.created'

    def __init__(self, skill_rule_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(skill_rule_id)}
        super().__init__(content, tenant_uuid)


class SkillRuleDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_rule_deleted'
    routing_key_fmt = 'config.queues.skillrules.deleted'

    def __init__(self, skill_rule_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(skill_rule_id)}
        super().__init__(content, tenant_uuid)


class SkillRuleEditedEvent(TenantEvent):
    service = 'confd'
    name = 'skill_rule_edited'
    routing_key_fmt = 'config.queues.skillrules.edited'

    def __init__(self, skill_rule_id: int, tenant_uuid: UUIDStr):
        content = {'id': int(skill_rule_id)}
        super().__init__(content, tenant_uuid)
