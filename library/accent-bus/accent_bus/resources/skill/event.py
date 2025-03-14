# resources/skill/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent


class SkillEvent(TenantEvent):
    """Base class for Skill events."""

    service: ClassVar[str] = "confd"
    content: dict


class SkillCreatedEvent(SkillEvent):
    """Event for when a skill is created."""

    name: ClassVar[str] = "skill_created"
    routing_key_fmt: ClassVar[str] = "config.agents.skills.created"

    def __init__(self, skill_id: int, **data):
        content = {"id": int(skill_id)}
        super().__init__(content=content, **data)


class SkillDeletedEvent(SkillEvent):
    """Event for when a skill is deleted."""

    name: ClassVar[str] = "skill_deleted"
    routing_key_fmt: ClassVar[str] = "config.agents.skills.deleted"

    def __init__(self, skill_id: int, **data):
        content = {"id": int(skill_id)}
        super().__init__(content=content, **data)


class SkillEditedEvent(SkillEvent):
    """Event for when a skill is edited."""

    name: ClassVar[str] = "skill_edited"
    routing_key_fmt: ClassVar[str] = "config.agents.skills.edited"

    def __init__(self, skill_id: int, **data):
        content = {"id": int(skill_id)}
        super().__init__(content=content, **data)
