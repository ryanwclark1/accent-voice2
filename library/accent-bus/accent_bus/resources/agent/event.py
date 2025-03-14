# resources/agent/event.py
from typing import ClassVar

from pydantic import Field
from resources.common.event import (
    MultiUserEvent,
    TenantEvent,
)  # Import base classes


class AgentEvent(TenantEvent):
    """Base class for Agent events."""

    # tenant_uuid is already defined.
    # No longer needed, but good practice to keep as a marker


class TenantAgentEvent(AgentEvent):
    """Base class for Tenant Agent Events."""

    service: ClassVar[str] = "confd"


class AgentCreatedEvent(TenantAgentEvent):
    """Event for when a new agent has been created."""

    name: ClassVar[str] = "agent_created"
    routing_key_fmt: ClassVar[str] = "config.agent.created"
    agent_id: int = Field(alias="id")
    content: dict = {}  # Add a content attribute, as all events should have it


class AgentDeletedEvent(TenantAgentEvent):
    """Event for when an agent has been deleted."""

    name: ClassVar[str] = "agent_deleted"
    routing_key_fmt: ClassVar[str] = "config.agent.deleted"
    agent_id: int = Field(alias="id")
    content: dict = {}


class AgentEditedEvent(TenantAgentEvent):
    """Event for when an agent has been edited."""

    name: ClassVar[str] = "agent_edited"
    routing_key_fmt: ClassVar[str] = "config.agent.edited"
    agent_id: int = Field(alias="id")
    content: dict = {}


class MultiUserAgentEvent(MultiUserEvent):
    """Base class for Agent events targeting multiple users."""

    service: ClassVar[str] = "agentd"  # Using agentd as in original.
    # user_uuids is already defined in MultiUserEvent
    content: dict = {}


class AgentPausedEvent(MultiUserAgentEvent):
    """Event for when an agent was paused."""

    name: ClassVar[str] = "agent_paused"
    routing_key_fmt: ClassVar[str] = "status.agent.pause"
    agent_id: int
    agent_number: str
    queue: str
    reason: str
    content: dict = {}


class AgentUnpausedEvent(MultiUserAgentEvent):
    """Event for when an agent was unpaused."""

    name: ClassVar[str] = "agent_unpaused"
    routing_key_fmt: ClassVar[str] = "status.agent.unpause"
    agent_id: int
    agent_number: str
    queue: str
    reason: str
    content: dict = {}


class AgentStatusUpdatedEvent(MultiUserAgentEvent):
    """Event for when an agent status has changed."""

    name: ClassVar[str] = "agent_status_update"
    routing_key_fmt: ClassVar[str] = "status.agent"
    agent_id: int
    status: str
    content: dict = {}
