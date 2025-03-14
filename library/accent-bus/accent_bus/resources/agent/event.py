# accent_bus/resources/agent/event.py
# Copyright 2025 Accent Communications

"""Agent events."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_bus.resources.common.event import MultiUserEvent, TenantEvent

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr


class AgentCreatedEvent(TenantEvent):
    """A new agent has been created."""

    service = "confd"
    name = "agent_created"
    routing_key_fmt = "config.agent.created"

    def __init__(self, agent_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Agent Created Event.

        Args:
           agent_id: ID of the new agent.
           tenant_uuid: Tenant UUID.

        """
        content = {"id": int(agent_id)}
        super().__init__(content, tenant_uuid)


class AgentDeletedEvent(TenantEvent):
    """An agent has been deleted."""

    service = "confd"
    name = "agent_deleted"
    routing_key_fmt = "config.agent.deleted"

    def __init__(self, agent_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Agent Deleted Event.

        Args:
           agent_id: ID of the deleted agent.
           tenant_uuid: Tenant UUID

        """
        content = {"id": int(agent_id)}
        super().__init__(content, tenant_uuid)


class AgentEditedEvent(TenantEvent):
    """An agent has been edited."""

    service = "confd"
    name = "agent_edited"
    routing_key_fmt = "config.agent.edited"

    def __init__(self, agent_id: int, tenant_uuid: UUIDStr) -> None:
        """Initialize Agent Edited Event.

        Args:
           agent_id: Agent ID
           tenant_uuid: Tenant UUID

        """
        content = {"id": int(agent_id)}
        super().__init__(content, tenant_uuid)


class AgentPausedEvent(MultiUserEvent):
    """An agent was paused."""

    service = "agentd"
    name = "agent_paused"
    routing_key_fmt = "status.agent.pause"
    required_acl_fmt = "events.statuses.agents"

    def __init__(
        self,
        agent_id: int,
        agent_number: str,
        queue: str,
        reason: str,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ) -> None:
        """Initialize Agent Paused Event.

        Args:
            agent_id: Agent ID
            agent_number: Agent Number
            queue: Queue name
            reason: Pause reason
            tenant_uuid: Tenant UUID
            user_uuids: List of User UUIDs

        """
        content = {
            "agent_id": agent_id,
            "agent_number": agent_number,
            "paused": True,
            "paused_reason": reason or "",
            "queue": queue,
        }
        super().__init__(content, tenant_uuid, user_uuids)


class AgentUnpausedEvent(MultiUserEvent):
    """An agent was unpaused."""

    service = "agentd"
    name = "agent_unpaused"
    routing_key_fmt = "status.agent.unpause"
    required_acl_fmt = "events.statuses.agents"

    def __init__(
        self,
        agent_id: int,
        agent_number: str,
        queue: str,
        reason: str,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ) -> None:
        """Initialize Agent Unpaused Event.

        Args:
            agent_id: Agent ID.
            agent_number: Agent Number.
            queue: Queue name.
            reason: Unpause reason.
            tenant_uuid: Tenant UUID
            user_uuids: List of User UUIDs.

        """
        content = {
            "agent_id": agent_id,
            "agent_number": agent_number,
            "paused": False,
            "paused_reason": reason or "",
            "queue": queue,
        }
        super().__init__(content, tenant_uuid, user_uuids)


class AgentStatusUpdatedEvent(MultiUserEvent):
    """An agent status has changed."""

    service = "calld"
    name = "agent_status_update"
    routing_key_fmt = "status.agent"
    required_acl_fmt = "events.statuses.agents"

    def __init__(
        self,
        agent_id: int,
        status: str,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ) -> None:
        """Initialize Agent Status Updated Event.

        Args:
            agent_id: Agent ID.
            status: Agent status
            tenant_uuid: Tenant UUID.
            user_uuids: List of user UUIDs.

        """
        content = {"agent_id": int(agent_id), "status": status}
        super().__init__(content, tenant_uuid, user_uuids)
