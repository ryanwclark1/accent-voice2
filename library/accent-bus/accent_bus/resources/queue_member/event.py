# resources/queue_member/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent, UserEvent


class QueueMemberEvent(TenantEvent):
    """Base class for Queue Member events."""

    service: ClassVar[str] = "confd"
    content: dict


class QueueMemberAgentAssociatedEvent(QueueMemberEvent):
    """Event for when an agent is associated as a member of a queue."""

    name: ClassVar[str] = "queue_member_agent_associated"
    routing_key_fmt: ClassVar[str] = "config.queues.agents.updated"

    def __init__(
        self,
        queue_id: int,
        agent_id: int,
        penalty: int,
        **data,
    ):
        content = {
            "queue_id": queue_id,
            "agent_id": agent_id,
            "penalty": penalty,
        }
        super().__init__(content=content, **data)


class QueueMemberAgentDissociatedEvent(QueueMemberEvent):
    """Event for when an agent is dissociated as a member of a queue."""

    name: ClassVar[str] = "queue_member_agent_dissociated"
    routing_key_fmt: ClassVar[str] = "config.queues.agents.deleted"

    def __init__(
        self,
        queue_id: int,
        agent_id: int,
        **data,
    ):
        content = {
            "queue_id": queue_id,
            "agent_id": agent_id,
        }
        super().__init__(content=content, **data)


class QueueMemberUserAssociatedEvent(UserEvent):  # Correct: Inherits from UserEvent
    """Event for when a *user* is associated as a member of a queue."""

    name: ClassVar[str] = "queue_member_user_associated"
    routing_key_fmt: ClassVar[str] = "config.queues.users.updated"
    service: ClassVar[str] = "confd"
    content: dict

    def __init__(
        self,
        queue_id: int,
        **data,
    ):
        content = {
            "queue_id": queue_id,
            "user_uuid": str(data["user_uuid"]),  # Get from kwargs
        }
        super().__init__(content=content, **data)


class QueueMemberUserDissociatedEvent(UserEvent):  # Correct: Inherits from UserEvent
    """Event for when a *user* is dissociated as a member of a queue."""

    name: ClassVar[str] = "queue_member_user_dissociated"
    routing_key_fmt: ClassVar[str] = "config.queues.users.deleted"
    service: ClassVar[str] = "confd"
    content: dict

    def __init__(
        self,
        queue_id: int,
        **data,
    ):
        content = {
            "queue_id": queue_id,
            "user_uuid": str(data["user_uuid"]),  # Get from kwargs
        }
        super().__init__(content=content, **data)
