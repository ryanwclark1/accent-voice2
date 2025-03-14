# resources/agent/event.py
from typing import ClassVar

from pydantic import Field

from accent_bus.resources.common.event import (  # Import base classes
    MultiUserEvent,
    TenantEvent,
)


class AgentEvent(TenantEvent):
    """Base class for Agent events."""

    # Tenant UUID is already defined in the parent class.
    pass  # noqa: PIE790


class TenantAgentEvent(AgentEvent):
    """Base class for Tenant Agent Events."""

    service: ClassVar[str] = "confd"


class AgentCreatedEvent(TenantAgentEvent):
    """Event for when a new agent has been created."""

    name: ClassVar[str] = "agent_created"
    routing_key_fmt: ClassVar[str] = "config.agent.created"
    agent_id: int = Field(alias="id")


class AgentDeletedEvent(TenantAgentEvent):
    """Event for when an agent has been deleted."""

    name: ClassVar[str] = "agent_deleted"
    routing_key_fmt: ClassVar[str] = "config.agent.deleted"
    agent_id: int = Field(alias="id")


class AgentEditedEvent(TenantAgentEvent):
    """Event for when an agent has been edited."""

    name: ClassVar[str] = "agent_edited"
    routing_key_fmt: ClassVar[str] = "config.agent.edited"
    agent_id: int = Field(alias="id")


class MultiUserAgentEvent(MultiUserEvent):
    """Base class for Agent events targeting multiple users."""

    service: ClassVar[str] = "agentd"  # Using agentd as in original.
    # user_uuids is already defined in MultiUserEvent


class AgentPausedEvent(MultiUserAgentEvent):
    """Event for when an agent was paused."""

    name: ClassVar[str] = "agent_paused"
    routing_key_fmt: ClassVar[str] = "status.agent.pause"
    agent_id: int
    agent_number: str
    queue: str
    reason: str


class AgentUnpausedEvent(MultiUserAgentEvent):
    """Event for when an agent was unpaused."""

    name: ClassVar[str] = "agent_unpaused"
    routing_key_fmt: ClassVar[str] = "status.agent.unpause"
    agent_id: int
    agent_number: str
    queue: str
    reason: str


class AgentStatusUpdatedEvent(MultiUserAgentEvent):
    """Event for when an agent status has changed."""

    name: ClassVar[str] = "agent_status_update"
    routing_key_fmt: ClassVar[str] = "status.agent"
    agent_id: int
    status: str
