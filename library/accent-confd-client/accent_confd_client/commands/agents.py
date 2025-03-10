# Copyright 2025 Accent Communications

"""Agents command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import AgentSkillRelation
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class AgentRelation:
    """Relations for agents."""

    def __init__(self, builder: Any, agent_id: str) -> None:
        """Initialize agent relations.

        Args:
            builder: Client instance
            agent_id: Agent ID

        """
        self.agent_id = agent_id
        self.agent_skill = AgentSkillRelation(builder)

    @extract_id
    def add_skill(self, skill_id: str, **kwargs: Any) -> Any:
        """Add a skill to the agent.

        Args:
            skill_id: Skill ID
            **kwargs: Additional parameters

        Returns:
            API response

        """
        return self.agent_skill.associate(self.agent_id, skill_id, **kwargs)

    @extract_id
    async def add_skill_async(self, skill_id: str, **kwargs: Any) -> Any:
        """Add a skill to the agent asynchronously.

        Args:
            skill_id: Skill ID
            **kwargs: Additional parameters

        Returns:
            API response

        """
        return await self.agent_skill.associate_async(self.agent_id, skill_id, **kwargs)

    @extract_id
    def remove_skill(self, skill_id: str) -> Any:
        """Remove a skill from the agent.

        Args:
            skill_id: Skill ID

        Returns:
            API response

        """
        return self.agent_skill.dissociate(self.agent_id, skill_id)

    @extract_id
    async def remove_skill_async(self, skill_id: str) -> Any:
        """Remove a skill from the agent asynchronously.

        Args:
            skill_id: Skill ID

        Returns:
            API response

        """
        return await self.agent_skill.dissociate_async(self.agent_id, skill_id)


class AgentsCommand(MultiTenantCommand):
    """Command for managing agents."""

    resource = "agents"
    relation_cmd = AgentRelation

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List agents asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of agents

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str, **kwargs: Any) -> dict[str, Any]:
        """Get an agent by ID asynchronously.

        Args:
            resource_id: Agent ID
            **kwargs: Additional parameters

        Returns:
            Agent data

        """
        return await super().get_async(resource_id, **kwargs)

    async def create_async(self, body: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Create an agent asynchronously.

        Args:
            body: Agent data
            **kwargs: Additional parameters

        Returns:
            Created agent data

        """
        return await super().create_async(body, **kwargs)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update an agent asynchronously.

        Args:
            body: Agent data

        """
        await super().update_async(body)

    async def delete_async(self, resource_id: str) -> None:
        """Delete an agent asynchronously.

        Args:
            resource_id: Agent ID

        """
        await super().delete_async(resource_id)
