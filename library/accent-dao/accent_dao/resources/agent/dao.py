# file: accent_dao/resources/agent/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.agentfeatures import AgentFeatures
from accent_dao.alchemy.agentqueueskill import AgentQueueSkill
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import AgentPersistor
from .search import agent_search


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for agents.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.

    """
    return await AgentPersistor(session, agent_search, tenant_uuids).search(parameters)


@async_daosession
async def get(
    session: AsyncSession, agent_id: int | str, tenant_uuids: list[str] | None = None
) -> AgentFeatures:
    """Get an agent by ID.

    Args:
        session:  The database session.
        agent_id:  The ID of the agent.
        tenant_uuids:  Optional list of tenant UUIDs to filter by.

    Returns:
        AgentFeatures:  The agent.

    """
    return await AgentPersistor(session, agent_search, tenant_uuids).get_by(
        {"id": int(agent_id)}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> AgentFeatures:
    """Get an agent by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        AgentFeatures: The agent.

    """
    return await AgentPersistor(session, agent_search, tenant_uuids).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession, agent_id: int | str, tenant_uuids: list[str] | None = None
) -> AgentFeatures | None:
    """Find an agent by ID.

    Args:
        session:  The database session.
        agent_id:  The ID of the agent.
        tenant_uuids:  Optional list of tenant UUIDs to filter by.

    Returns:
        AgentFeatures | None: The agent, or None if not found.

    """
    return await AgentPersistor(session, agent_search, tenant_uuids).find_by(
        {"id": int(agent_id)}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> AgentFeatures | None:
    """Find an agent by criteria.

    Args:
        session:  The database session.
        tenant_uuids:  Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        AgentFeatures | None: The agent, or None if not found.

    """
    return await AgentPersistor(session, agent_search, tenant_uuids).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[AgentFeatures]:
    """Find all agents by criteria.

    Args:
        session:  The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        list[AgentFeatures]: A list of agents.

    """
    return await AgentPersistor(session, agent_search, tenant_uuids).find_all_by(
        criteria
    )


@async_daosession
async def create(session: AsyncSession, agent: AgentFeatures) -> AgentFeatures:
    """Create a new agent.

    Args:
        session:  The database session.
        agent:  The agent to create.

    Returns:
        AgentFeatures: The created agent.

    """
    return await AgentPersistor(session, agent_search).create(agent)


@async_daosession
async def edit(session: AsyncSession, agent: AgentFeatures) -> None:
    """Edit an existing agent.

    Args:
        session:  The database session.
        agent: The agent to edit.

    """
    await AgentPersistor(session, agent_search).edit(agent)


@async_daosession
async def delete(session: AsyncSession, agent: AgentFeatures) -> None:
    """Delete an agent.

    Args:
        session: The database session.
        agent: The agent to delete.

    """
    await AgentPersistor(session, agent_search).delete(agent)


@async_daosession
async def associate_agent_skill(
    session: AsyncSession, agent: AgentFeatures, agent_skill: AgentQueueSkill
) -> None:
    """Associate an agent skill with an agent.

    Args:
        session: The database session.
        agent: The agent.
        agent_skill: The agent skill to associate.

    """
    await AgentPersistor(session, agent_search).associate_agent_skill(
        agent, agent_skill
    )


@async_daosession
async def dissociate_agent_skill(
    session: AsyncSession, agent: AgentFeatures, agent_skill: AgentQueueSkill
) -> None:
    """Dissociate an agent skill from an agent.

    Args:
        session: The database session.
        agent: The agent.
        agent_skill: The agent skill to dissociate.

    """
    await AgentPersistor(session, agent_search).dissociate_agent_skill(
        agent, agent_skill
    )
