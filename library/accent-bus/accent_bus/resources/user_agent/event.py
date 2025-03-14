# resources/user_agent/event.py
from typing import ClassVar

from resources.common.event import UserEvent


class UserAgentEvent(UserEvent):
    """Base class for User Agent events."""

    service: ClassVar[str] = "confd"
    content: dict


class UserAgentAssociatedEvent(UserAgentEvent):
    """Event for when an agent is associated with a user."""

    name: ClassVar[str] = "user_agent_associated"
    routing_key_fmt: ClassVar[str] = "config.users.{user_uuid}.agents.updated"

    def __init__(self, agent_id: int, **data):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "agent_id": agent_id,
        }
        super().__init__(content=content, **data)


class UserAgentDissociatedEvent(UserAgentEvent):
    """Event for when an agent is dissociated from a user."""

    name: ClassVar[str] = "user_agent_dissociated"
    routing_key_fmt: ClassVar[str] = "config.users.{user_uuid}.agents.deleted"

    def __init__(self, agent_id: int, **data):
        content = {
            "user_uuid": str(data["user_uuid"]),
            "agent_id": agent_id,
        }
        super().__init__(content=content, **data)
