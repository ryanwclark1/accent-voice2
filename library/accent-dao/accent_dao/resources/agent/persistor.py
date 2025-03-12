# file: accent_dao/resources/agent/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.agentfeatures import AgentFeatures as Agent
from accent_dao.alchemy.agentqueueskill import AgentQueueSkill
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence


class AgentPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Agent]):
    """Persistor class for Agent model."""

    _search_table = Agent

    def __init__(
        self,
        session: AsyncSession,
        agent_search: Any,  # Use Any for now
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize AgentPersistor.

        Args:
            session: Async database session.
            agent_search: Search system for agents.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = agent_search
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find agents based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Agent)  # Use select for async
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> Agent:
        """Retrieve a single agent by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Agent: The found agent.

        Raises:
            NotFoundError: If no agent is found.

        """
        agent = await self.find_by(criteria)
        if not agent:
            raise errors.NotFoundError("Agent", **criteria)
        return agent

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for agents.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = select(Agent)  # Use select for async
        if self.tenant_uuids is not None:
            query = query.filter(Agent.tenant_uuid.in_(self.tenant_uuids))
        return await self.search_system.async_search_from_query(
            self.session, query, parameters
        )

    async def associate_agent_skill(
        self, agent: Agent, agent_skill: AgentQueueSkill
    ) -> None:
        """Associate an agent skill with an agent.

        Args:
            agent: The agent object.
            agent_skill: The agent skill object.

        """
        if agent_skill not in agent.agent_queue_skills:
            agent.agent_queue_skills.append(agent_skill)
        await self.session.flush()

    async def dissociate_agent_skill(
        self, agent: Agent, agent_skill: AgentQueueSkill
    ) -> None:
        """Dissociate an agent skill from an agent.

        Args:
            agent: The agent object.
            agent_skill: The agent skill object.

        """
        try:
            agent.agent_queue_skills.remove(agent_skill)
            await self.session.flush()
        except ValueError:
            pass

    def _filter_tenant_uuid(self, query: Any) -> Any:
        """Filter query by tenant UUID.

        Args:
            query: The query object.

        Returns:
            The filtered query object.

        """
        if self.tenant_uuids is not None:
            query = query.filter(Agent.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Agent]:
        """Find all AccessFeatures by criteria.

        Returns:
            list of AccessFeatures.

        """
        result: Sequence[Agent] = await super().find_all_by(criteria)
        return list(result)
