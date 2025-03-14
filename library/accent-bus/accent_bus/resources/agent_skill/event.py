# resources/agent_skill/event.py
from typing import ClassVar

from pydantic import Field  # Import Field

from accent_bus.resources.common.event import TenantEvent


class AgentSkillEvent(TenantEvent):
    """Base class for Agent Skill events."""

    service: ClassVar[str] = "confd"
    content: dict  # It will be a dict, since the content is not typed


class AgentSkillAssociatedEvent(AgentSkillEvent):
    """Event for when an agent skill is associated."""

    name: ClassVar[str] = "agent_skill_associated"
    routing_key_fmt: ClassVar[str] = "config.agents.skills.updated"
    agent_id: int = Field(...)
    skill_id: int = Field(...)

    def __init__(self, agent_id: int, skill_id: int, **data):
        content = {
            "agent_id": agent_id,
            "skill_id": skill_id,
        }
        super().__init__(content=content, **data)


class AgentSkillDissociatedEvent(AgentSkillEvent):
    """Event for when an agent skill is dissociated."""

    name: ClassVar[str] = "agent_skill_dissociated"
    routing_key_fmt: ClassVar[str] = "config.agents.skills.deleted"
    agent_id: int = Field(...)
    skill_id: int = Field(...)

    def __init__(self, agent_id: int, skill_id: int, **data):
        content = {
            "agent_id": agent_id,
            "skill_id": skill_id,
        }
        super().__init__(content=content, **data)
