# accent_dao/dao/queue_member_dao.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import func, select

from accent_dao.alchemy.queuemember import QueueMember
from accent_dao.helpers.db_manager import async_daosession, daosession
from accent_dao.helpers.db_utils import async_flush_session, flush_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@daosession
def add_agent_to_queue(
    session: Session, agent_id: int, agent_number: str, queue_name: str
) -> None:
    """Add agent to specified queue.

    Args:
        session: Database session (injected by decorator)
        agent_id: ID of the agent to add
        agent_number: Agent's phone number
        queue_name: Name of the queue to add agent to

    Returns:
        None

    """
    next_position = _get_next_position_for_queue(session, queue_name)
    queue_member = QueueMember()
    queue_member.queue_name = queue_name
    queue_member.interface = f"Agent/{agent_number}"
    queue_member.usertype = "agent"
    queue_member.userid = agent_id
    queue_member.channel = "Agent"
    queue_member.category = "queue"
    queue_member.position = next_position

    with flush_session(session):
        session.add(queue_member)


@async_daosession
async def add_agent_to_queue_async(
    session: AsyncSession, agent_id: int, agent_number: str, queue_name: str
) -> None:
    """Add agent to specified queue asynchronously.

    Args:
        session: Async database session (injected by decorator)
        agent_id: ID of the agent to add
        agent_number: Agent's phone number
        queue_name: Name of the queue to add agent to

    Returns:
        None

    """
    next_position = await _get_next_position_for_queue_async(session, queue_name)
    queue_member = QueueMember()
    queue_member.queue_name = queue_name
    queue_member.interface = f"Agent/{agent_number}"
    queue_member.usertype = "agent"
    queue_member.userid = agent_id
    queue_member.channel = "Agent"
    queue_member.category = "queue"
    queue_member.position = next_position

    async with async_flush_session(session):
        session.add(queue_member)


@daosession
def remove_agent_from_queue(session: Session, agent_id: int, queue_name: str) -> None:
    """Remove agent from specified queue.

    Args:
        session: Database session (injected by decorator)
        agent_id: ID of the agent to remove
        queue_name: Name of the queue to remove agent from

    Returns:
        None

    """
    # Updated to use SQLAlchemy 2.x style
    stmt = (
        select(QueueMember)
        .where(QueueMember.queue_name == queue_name)
        .where(QueueMember.usertype == "agent")
        .where(QueueMember.userid == agent_id)
    )

    result = session.execute(stmt)
    for queue_member in result.scalars().all():
        session.delete(queue_member)


@async_daosession
async def remove_agent_from_queue_async(
    session: AsyncSession, agent_id: int, queue_name: str
) -> None:
    """Remove agent from specified queue asynchronously.

    Args:
        session: Async database session (injected by decorator)
        agent_id: ID of the agent to remove
        queue_name: Name of the queue to remove agent from

    Returns:
        None

    """
    # SQLAlchemy 2.x style
    stmt = (
        select(QueueMember)
        .where(QueueMember.queue_name == queue_name)
        .where(QueueMember.usertype == "agent")
        .where(QueueMember.userid == agent_id)
    )

    result = await session.execute(stmt)
    for queue_member in result.scalars().all():
        await session.delete(queue_member)


def _get_next_position_for_queue(session: Session, queue_name: str) -> int:
    """Get next available position for a queue member.

    Args:
        session: Database session
        queue_name: Name of the queue

    Returns:
        int: Next available position number

    """
    # Updated to use SQLAlchemy 2.x style
    stmt = select(func.max(QueueMember.position).label("max")).where(
        QueueMember.queue_name == queue_name
    )

    result = session.execute(stmt).one_or_none()
    last_position = result[0] if result else None

    if last_position is None:
        return 0
    return last_position + 1


async def _get_next_position_for_queue_async(
    session: AsyncSession, queue_name: str
) -> int:
    """Get next available position for a queue member asynchronously.

    Args:
        session: Async database session
        queue_name: Name of the queue

    Returns:
        int: Next available position number

    """
    # SQLAlchemy 2.x style
    stmt = select(func.max(QueueMember.position).label("max")).where(
        QueueMember.queue_name == queue_name
    )

    result = await session.execute(stmt)
    row = result.one_or_none()
    last_position = row[0] if row else None

    if last_position is None:
        return 0
    return last_position + 1
