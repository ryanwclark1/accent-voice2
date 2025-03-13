# File: accent_dao/alchemy/stat_agent_dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

"""Data access operations for StatAgent model."""

import logging
from typing import NamedTuple, TypedDict

from sqlalchemy import distinct, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import or_

from accent_dao.alchemy.stat_agent import StatAgent

logger = logging.getLogger(__name__)

class AgentKey(NamedTuple):
    """A NamedTuple representing the key for an agent.

    Attributes:
        name (str): The name of the agent.
        tenant_uuid (str): The UUID of the tenant associated with the agent.

    """

    name: str
    tenant_uuid: str


class ConfdAgent(TypedDict):
    """Type definition for agent data from ConFD."""

    id: str
    number: str
    tenant_uuid: str


async def insert_missing_agents(
    session: AsyncSession, confd_agents: list[ConfdAgent]
) -> None:
    """Insert missing agents into the database based on confd agents.

    Args:
        session: The database session.
        confd_agents: List of agents from ConFD.

    """
    confd_agents_by_key = {
        AgentKey(f"Agent/{agent['number']}", agent["tenant_uuid"]): agent
        for agent in confd_agents
    }

    await _mark_recreated_agents_with_same_number_as_deleted(
        session, confd_agents_by_key
    )
    await _mark_non_confd_agents_as_deleted(session, confd_agents_by_key)
    await _create_missing_agents(session, confd_agents_by_key)
    await _rename_deleted_agents_with_duplicate_name(session, confd_agents_by_key)


async def _mark_recreated_agents_with_same_number_as_deleted(
    session: AsyncSession, confd_agents_by_key: dict[AgentKey, ConfdAgent]
) -> None:
    """Mark agents that have been recreated with the same number as deleted.

    Args:
        session: The database session.
        confd_agents_by_key: Dictionary of agents from ConFD by AgentKey.

    """
    db_agent_query = select(StatAgent).where(StatAgent.deleted.is_(False))
    result = await session.execute(db_agent_query)
    db_agents = result.scalars().all()

    db_agents_by_name = {
        AgentKey(agent.name, agent.tenant_uuid): agent for agent in db_agents
    }

    existing_in_confd = set(confd_agents_by_key.keys())
    existing_in_stat_agent = set(db_agents_by_name.keys())

    not_missing_agents = existing_in_confd.intersection(existing_in_stat_agent)
    for agent_key in not_missing_agents:
        confd_agent = confd_agents_by_key[agent_key]
        db_agent = db_agents_by_name[agent_key]
        if db_agent.agent_id != confd_agent["id"]:
            db_agent.deleted = True
            await session.flush()


async def _mark_non_confd_agents_as_deleted(
    session: AsyncSession, confd_agents_by_key: dict[AgentKey, ConfdAgent]
) -> None:
    """Mark agents that don't exist in ConFD as deleted.

    Args:
        session: The database session.
        confd_agents_by_key: Dictionary of agents from ConFD by AgentKey.

    """
    active_agent_ids = {agent["id"] for agent in confd_agents_by_key.values()}

    agent_ids_query = select(distinct(StatAgent.agent_id))
    result = await session.execute(agent_ids_query)
    all_agent_ids = {r[0] for r in result}

    deleted_agents = [
        agent for agent in list(all_agent_ids - active_agent_ids) if agent
    ]

    if deleted_agents or any(1 for _ in all_agent_ids if _ is None):
        update_stmt = select(StatAgent).where(
            or_(
                StatAgent.agent_id.in_(deleted_agents),
                StatAgent.agent_id.is_(None),
            )
        )
        result = await session.execute(update_stmt)
        agents_to_update = result.scalars().all()

        for agent in agents_to_update:
            if isinstance(agent, StatAgent):
                agent.deleted = True

        await session.flush()


async def _create_missing_agents(
    session: AsyncSession, confd_agents_by_key: dict[AgentKey, ConfdAgent]
) -> None:
    """Create missing agents in the database.

    Args:
        session: The database session.
        confd_agents_by_key: Dictionary of agents from ConFD by AgentKey.

    """
    new_agent_keys = set(confd_agents_by_key.keys())

    db_agent_query = select(StatAgent).where(StatAgent.deleted.is_(False))
    result = await session.execute(db_agent_query)
    db_agents = result.scalars().all()

    old_agent_keys = {AgentKey(agent.name, agent.tenant_uuid) for agent in db_agents}

    missing_agents = list(new_agent_keys - old_agent_keys)
    for agent_key in missing_agents:
        agent = confd_agents_by_key[agent_key]
        new_agent = StatAgent()
        new_agent.name = agent_key.name
        new_agent.tenant_uuid = agent["tenant_uuid"]
        new_agent.agent_id = agent["id"]
        new_agent.deleted = False
        session.add(new_agent)

    if missing_agents:
        logger.info("Creating %d missing agents", len(missing_agents))
        await session.flush()


async def _rename_deleted_agents_with_duplicate_name(
    session: AsyncSession, confd_agents_by_key: dict[AgentKey, ConfdAgent]
) -> None:
    """Rename deleted agents that have duplicate names.

    Args:
        session: The database session.
        confd_agents_by_key: Dictionary of agents from ConFD by AgentKey.

    """
    db_agent_query = select(StatAgent).where(StatAgent.deleted.is_(True))
    result = await session.execute(db_agent_query)
    db_agents = result.scalars().all()

    for agent in db_agents:
        if AgentKey(agent.name, agent.tenant_uuid) in confd_agents_by_key:
            agent.name = await _find_next_available_name(
                session, agent.name, agent.tenant_uuid
            )

    await session.flush()


async def _find_next_available_name(
    session: AsyncSession, name: str, tenant_uuid: str
) -> str:
    """Find the next available name for an agent.

    Args:
        session: The database session.
        name: Current name to check.
        tenant_uuid: Tenant UUID.

    Returns:
        str: Next available name.

    """
    query = select(StatAgent).where(
        StatAgent.name == name,
        StatAgent.tenant_uuid == tenant_uuid,
    )

    result = await session.execute(query)
    if result.first():
        next_name = f"{name}_"
        return await _find_next_available_name(session, next_name, tenant_uuid)

    return name


async def clean_table(session: AsyncSession) -> None:
    """Delete all records from the StatAgent table.

    Args:
        session: The database session.

    """
    delete_stmt = select(StatAgent)
    result = await session.execute(delete_stmt)
    agents = result.scalars().all()

    for agent in agents:
        await session.delete(agent)
