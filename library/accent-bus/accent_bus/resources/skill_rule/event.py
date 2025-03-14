# resources/skill_rule/event.py
from typing import ClassVar

from resources.common.event import TenantEvent


class SkillRuleEvent(TenantEvent):
    """Base class for Skill Rule events."""

    service: ClassVar[str] = "confd"
    content: dict


class SkillRuleCreatedEvent(SkillRuleEvent):
    """Event for when a skill rule is created."""

    name: ClassVar[str] = "skill_rule_created"
    routing_key_fmt: ClassVar[str] = "config.queues.skillrules.created"

    def __init__(self, skill_rule_id: int, **data):
        content = {"id": int(skill_rule_id)}
        super().__init__(content=content, **data)


class SkillRuleDeletedEvent(SkillRuleEvent):
    """Event for when a skill rule is deleted."""

    name: ClassVar[str] = "skill_rule_deleted"
    routing_key_fmt: ClassVar[str] = "config.queues.skillrules.deleted"

    def __init__(self, skill_rule_id: int, **data):
        content = {"id": int(skill_rule_id)}
        super().__init__(content=content, **data)


class SkillRuleEditedEvent(SkillRuleEvent):
    """Event for when a skill rule is edited."""

    name: ClassVar[str] = "skill_rule_edited"
    routing_key_fmt: ClassVar[str] = "config.queues.skillrules.edited"

    def __init__(self, skill_rule_id: int, **data):
        content = {"id": int(skill_rule_id)}
        super().__init__(content=content, **data)
