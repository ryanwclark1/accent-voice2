# agent_dao.py
# Copyright 2025 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from sqlalchemy import and_, select

from accent_dao.alchemy.agentfeatures import AgentFeatures
from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.alchemy.queuemember import QueueMember
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import daosession

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import Session
    from sqlalchemy.sql.elements import BinaryExpression


class Agent(NamedTuple):
    """Agent data structure."""

    id: int
    tenant_uuid: str
    number: str
    queues: list[QueueFeatures]
    user_ids: list[int]


class Queue(NamedTuple):
    """Queue data structure."""

    id: int
    tenant_uuid: str
    name: str
    penalty: int


@daosession
def agent_with_id(
    session: Session,
    agent_id: int | str,
    tenant_uuids: list[str] | None = None,
) -> Agent:
    """Get agent by ID.

    Args:
        session: Database session
        agent_id: Agent ID
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        Agent with specified ID

    Raises:
        LookupError: If no agent found

    """
    agent = _get_agent(session, AgentFeatures.id == int(agent_id), tenant_uuids)
    _add_queues_to_agent(session, agent)
    return agent


@daosession
def agent_with_number(
    session: Session, agent_number: str, tenant_uuids: list[str] | None = None
) -> Agent:
    """Get agent by number.

    Args:
        session: Database session
        agent_number: Agent number
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        Agent with specified number

    Raises:
        LookupError: If no agent found

    """
    agent = _get_agent(session, AgentFeatures.number == agent_number, tenant_uuids)
    _add_queues_to_agent(session, agent)
    return agent


@daosession
def agent_with_user_uuid(
    session: Session, user_uuid: str, tenant_uuids: list[str] | None = None
) -> Agent:
    """Get agent by user UUID.

    Args:
        session: Database session
        user_uuid: User UUID
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        Agent with specified user UUID

    Raises:
        LookupError: If no agent found

    """
    query = (
        session.query(AgentFeatures)
        .join(UserFeatures, AgentFeatures.id == UserFeatures.agentid)
        .filter(UserFeatures.uuid == user_uuid)
    )
    if tenant_uuids is not None:
        query = query.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))

    agent_row = query.first()
    if agent_row is None:
        error_message = f"no agent found for user {user_uuid}"
        raise LookupError(error_message)
    agent = Agent(
        agent_row.id,
        agent_row.tenant_uuid,
        agent_row.number,
        [],
        [user.id for user in agent_row.users],
    )
    _add_queues_to_agent(session, agent)
    return agent




def _get_agent(
    session: Session,
    whereclause: BinaryExpression,
    tenant_uuids: list[str] | None = None
) -> Agent:
    query = session.query(AgentFeatures).filter(whereclause)
    if tenant_uuids is not None:
        query = query.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))
    agent = query.first()
    if agent is None:
        error_message = f"no agent matching clause {whereclause.compile().params}"
        raise LookupError(error_message)
    return Agent(
        agent.id, agent.tenant_uuid, agent.number, [], [user.id for user in agent.users]
    )


def _add_queues_to_agent(session: Session, agent: Agent) -> None:
    stmt = select(
        [
            QueueFeatures.id,
            QueueFeatures.tenant_uuid,
            QueueMember.queue_name,
            QueueMember.penalty,
        ]
    ).where(
        and_(
            QueueMember.usertype == "agent",
            QueueMember.userid == agent.id,
            QueueMember.queue_name == QueueFeatures.name,
        )
    )

    for row in session.execute(stmt):
        queue = Queue(row["id"], row["tenant_uuid"], row["queue_name"], row["penalty"])
        agent.queues.append(queue)


@daosession
def get(
    session: Session, agentid: int | str, tenant_uuids: list[str] | None = None
) -> AgentFeatures | None:
    """Get agent by ID.

    Args:
        session: Database session
        agentid: Agent ID
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        Agent or None if not found

    """
    query = session.query(AgentFeatures).filter(AgentFeatures.id == int(agentid))
    if tenant_uuids is not None:
        query = query.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))
    return query.first()


@daosession
def all(
    session: Session, tenant_uuids: list[str] | None = None
) -> Sequence[AgentFeatures]:
    """Get all agents.

    Args:
        session: Database session
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        List of agents

    """
    query = session.query(AgentFeatures)
    if tenant_uuids is not None:
        query = query.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))
    return query.all()


# Now add async versions


async def async_agent_with_id(
    session: AsyncSession,
    agent_id: int | str,
    tenant_uuids: list[str] | None = None,
) -> Agent:
    """Get agent by ID (async version).

    Args:
        session: Async database session
        agent_id: Agent ID
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        Agent with specified ID

    Raises:
        LookupError: If no agent found

    """
    agent = await async_get_agent(
        session, AgentFeatures.id == int(agent_id), tenant_uuids
    )
    await async_add_queues_to_agent(session, agent)
    return agent


async def async_agent_with_number(
    session: AsyncSession, agent_number: str, tenant_uuids: list[str] | None = None
) -> Agent:
    """Get agent by number (async version).

    Args:
        session: Async database session
        agent_number: Agent number
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        Agent with specified number

    Raises:
        LookupError: If no agent found

    """
    agent = await async_get_agent(
        session, AgentFeatures.number == agent_number, tenant_uuids
    )
    await async_add_queues_to_agent(session, agent)
    return agent


async def async_agent_with_user_uuid(
    session: AsyncSession, user_uuid: str, tenant_uuids: list[str] | None = None
) -> Agent:
    """Get agent by user UUID (async version).

    Args:
        session: Async database session
        user_uuid: User UUID
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        Agent with specified user UUID

    Raises:
        LookupError: If no agent found

    """
    stmt = (
        select(AgentFeatures)
        .join(UserFeatures, AgentFeatures.id == UserFeatures.agentid)
        .filter(UserFeatures.uuid == user_uuid)
    )
    if tenant_uuids is not None:
        stmt = stmt.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    agent_row = result.scalar_one_or_none()

    if agent_row is None:
        error_message = f"no agent found for user {user_uuid}"
        raise LookupError(error_message)

    agent = Agent(
        agent_row.id,
        agent_row.tenant_uuid,
        agent_row.number,
        [],
        [user.id for user in agent_row.users],
    )
    await async_add_queues_to_agent(session, agent)
    return agent


async def async_get_agent(
    session: AsyncSession,
    whereclause: BinaryExpression,
    tenant_uuids: list[str] | None = None
) -> Agent:
    """Get agent by where clause (async version).

    Args:
        session: Async database session
        whereclause: Where clause
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        Agent matching where clause

    Raises:
        LookupError: If no agent found

    """
    stmt = select(AgentFeatures).filter(whereclause)
    if tenant_uuids is not None:
        stmt = stmt.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    agent = result.scalar_one_or_none()

    if agent is None:
        error_message = f"no agent matching clause {whereclause}"
        raise LookupError(error_message)

    return Agent(
        agent.id, agent.tenant_uuid, agent.number, [], [user.id for user in agent.users]
    )


async def async_add_queues_to_agent(session: AsyncSession, agent: Agent) -> None:
    """Add queues to agent (async version).

    Args:
        session: Async database session
        agent: Agent to add queues to

    """
    stmt = select(
        QueueFeatures.id,
        QueueFeatures.tenant_uuid,
        QueueMember.queue_name,
        QueueMember.penalty,
    ).where(
        and_(
            QueueMember.usertype == "agent",
            QueueMember.userid == agent.id,
            QueueMember.queue_name == QueueFeatures.name,
        )
    )

    result = await session.execute(stmt)
    for row in result:
        queue = Queue(row.id, row.tenant_uuid, row.queue_name, row.penalty)
        agent.queues.append(queue)


async def async_get(
    session: AsyncSession,
    agentid: int | str,
    tenant_uuids: list[str] | None = None,
) -> AgentFeatures | None:
    """Get agent by ID (async version).

    Args:
        session: Async database session
        agentid: Agent ID
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        Agent or None if not found

    """
    stmt = select(AgentFeatures).filter(AgentFeatures.id == int(agentid))
    if tenant_uuids is not None:
        stmt = stmt.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def async_all(
    session: AsyncSession, tenant_uuids: list[str] | None = None
) -> Sequence[AgentFeatures]:
    """Get all agents (async version).

    Args:
        session: Async database session
        tenant_uuids: Optional list of tenant UUIDs to filter by

    Returns:
        List of agents

    """
    stmt = select(AgentFeatures)
    if tenant_uuids is not None:
        stmt = stmt.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    return result.scalars().all()
