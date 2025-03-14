# resources/agent/event.py
from typing import ClassVar

from pydantic import BaseModel, Field

from accent_bus.resources.common.event import (
    MultiUserEvent,
    TenantEvent,
)  # Import base classes


class AgentEvent(TenantEvent):
    """Base class for Agent events."""

    # tenant_uuid is already defined in the parent class.
    content: dict  # Use dict when no specific Pydantic model for content


class TenantAgentEvent(AgentEvent):
    """Base class for Tenant Agent events."""

    service: ClassVar[str] = "confd"
    content: dict


class AgentCreatedEvent(TenantAgentEvent):
    """Event for when a new agent has been created."""

    name: ClassVar[str] = "agent_created"
    routing_key_fmt: ClassVar[str] = "config.agent.created"
    agent_id: int = Field(alias="id")  # Keep original "id" field name
    content: dict = {}

    def __init__(self, agent_id: int, **data):
        content = {"id": agent_id}
        super().__init__(content=content, **data)


class AgentDeletedEvent(TenantAgentEvent):
    """Event for when an agent has been deleted."""

    name: ClassVar[str] = "agent_deleted"
    routing_key_fmt: ClassVar[str] = "config.agent.deleted"
    agent_id: int = Field(alias="id")
    content: dict = {}

    def __init__(self, agent_id: int, **data):
        content = {"id": agent_id}
        super().__init__(content=content, **data)


class AgentEditedEvent(TenantAgentEvent):
    """Event for when an agent has been edited."""

    name: ClassVar[str] = "agent_edited"
    routing_key_fmt: ClassVar[str] = "config.agent.edited"
    agent_id: int = Field(alias="id")
    content: dict = {}

    def __init__(self, agent_id: int, **data):
        content = {"id": agent_id}
        super().__init__(content=content, **data)


class MultiUserAgentEvent(MultiUserEvent):
    """Base class for Agent events targeting multiple users."""

    service: ClassVar[str] = "agentd"  # Using agentd as in original.
    # user_uuids is already defined in MultiUserEvent
    content: dict = {}


class AgentPausedContent(BaseModel):
    """Content model for AgentPausedEvent."""

    agent_id: int
    agent_number: str
    queue: str
    paused: bool = True
    paused_reason: str


class AgentPausedEvent(MultiUserAgentEvent):
    """Event for when an agent was paused."""

    name: ClassVar[str] = "agent_paused"
    routing_key_fmt: ClassVar[str] = "status.agent.pause"
    content: AgentPausedContent

    def __init__(
        self, agent_id: int, agent_number: str, queue: str, reason: str, **data
    ):
        content = AgentPausedContent(
            agent_id=agent_id,
            agent_number=agent_number,
            queue=queue,
            paused_reason=reason,
        )
        super().__init__(content=content, **data)  # Pass the *instance*


class AgentUnpausedContent(BaseModel):
    """Content model for AgentUnpausedEvent."""

    agent_id: int
    agent_number: str
    queue: str
    paused: bool = False  # Explicitly set to False
    paused_reason: str


class AgentUnpausedEvent(MultiUserAgentEvent):
    """Event for when an agent was unpaused."""

    name: ClassVar[str] = "agent_unpaused"
    routing_key_fmt: ClassVar[str] = "status.agent.unpause"
    content: AgentUnpausedContent  # Use the Pydantic model

    def __init__(
        self, agent_id: int, agent_number: str, queue: str, reason: str, **data
    ):
        content = AgentUnpausedContent(
            agent_id=agent_id,
            agent_number=agent_number,
            queue=queue,
            paused_reason=reason,
        )
        super().__init__(content=content, **data)  # Pass instance


class AgentStatusUpdatedContent(BaseModel):
    """Content for agent status updated.

    Attributes:
        agent_id (int): Agent ID.
        status (str): Status.

    """

    agent_id: int
    status: str


class AgentStatusUpdatedEvent(MultiUserAgentEvent):
    """Event for when an agent status has changed."""

    name: ClassVar[str] = "agent_status_update"
    routing_key_fmt: ClassVar[str] = "status.agent"
    content: AgentStatusUpdatedContent

    def __init__(self, agent_id: int, status: str, **data):
        content = AgentStatusUpdatedContent(agent_id=agent_id, status=status)
        super().__init__(content=content, **data)  # Pass instance
