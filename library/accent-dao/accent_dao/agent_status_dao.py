# file: accent_dao/agent_status_dao.py # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, NamedTuple, cast

from sqlalchemy import case, false, select, true
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from accent_dao.alchemy.agent_login_status import AgentLoginStatus
from accent_dao.alchemy.agent_membership_status import AgentMembershipStatus
from accent_dao.alchemy.agentfeatures import AgentFeatures
from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.alchemy.queuemember import QueueMember
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.helpers.db_utils import async_flush_session

if TYPE_CHECKING:
    from collections.abc import Sequence


class Queue(NamedTuple):
    """Queue data structure.

    Attributes:
        id: Queue identifier
        name: Queue name
        penalty: Agent's penalty in this queue

    """

    id: int
    name: str
    penalty: int


class AgentStatus(NamedTuple):
    """Agent status data structure.

    Attributes:
        agent_id: Agent identifier
        agent_number: Agent number
        extension: Agent's extension
        context: Agent's context
        interface: Agent's interface
        state_interface: Agent's state interface
        login_at: Timestamp of agent login
        paused: Whether agent is paused
        paused_reason: Reason for agent's pause
        queues: List of queues agent belongs to
        user_ids: List of user IDs associated with the agent

    """

    agent_id: int
    agent_number: str
    extension: str
    context: str
    interface: str
    state_interface: str
    login_at: datetime
    paused: bool
    paused_reason: str | None
    queues: list[Queue] | None
    user_ids: list[int]


@async_daosession
async def get_status(
    session: AsyncSession, agent_id: int, tenant_uuids: list[str] | None = None
) -> AgentStatus | None:
    """Get status of an agent by ID.

    Args:
        session: Database session
        agent_id: Agent identifier
        tenant_uuids: Optional tenant identifiers to filter by

    Returns:
        Agent status or None if agent is not found

    """
    login_status = await _get_login_status_by_id(
        session, agent_id, tenant_uuids=tenant_uuids
    )
    if not login_status:
        return None

    queues = await _get_queues_for_agent(session, agent_id)
    return _to_agent_status(login_status, queues)


@async_daosession
async def get_status_by_number(
    session: AsyncSession, agent_number: str, tenant_uuids: list[str] | None = None
) -> AgentStatus | None:
    """Get status of an agent by number.

    Args:
        session: Database session
        agent_number: Agent number
        tenant_uuids: Optional tenant identifiers to filter by

    Returns:
        Agent status or None if agent is not found

    """
    login_status = await _get_login_status_by_number(
        session, agent_number, tenant_uuids=tenant_uuids
    )
    if not login_status:
        return None

    queues = await _get_queues_for_agent(session, login_status.agent_id)
    return _to_agent_status(login_status, queues)


@async_daosession
async def get_status_by_user(
    session: AsyncSession, user_uuid: str, tenant_uuids: list[str] | None = None
) -> AgentStatus | None:
    """Get status of an agent by user UUID.

    Args:
        session: Database session
        user_uuid: User identifier
        tenant_uuids: Optional tenant identifiers to filter by

    Returns:
        Agent status or None if agent is not found

    """
    login_status = await _get_login_status_by_user(
        session, user_uuid, tenant_uuids=tenant_uuids
    )
    if not login_status:
        return None

    queues = await _get_queues_for_agent(session, login_status.agent_id)
    return _to_agent_status(login_status, queues)


async def _get_login_status_by_id(
    session: AsyncSession, agent_id: int, tenant_uuids: list[str] | None = None
) -> AgentLoginStatus | None:
    """Get login status of an agent by ID.

    Args:
        session: Database session
        agent_id: Agent identifier
        tenant_uuids: Optional tenant identifiers to filter by

    Returns:
        Agent login status or None if not found

    """
    stmt = (
        select(AgentLoginStatus)
        .outerjoin(AgentFeatures, AgentFeatures.id == AgentLoginStatus.agent_id)
        .filter(AgentLoginStatus.agent_id == agent_id)
    )
    if tenant_uuids is not None:
        stmt = stmt.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    return result.scalars().first()


async def _get_login_status_by_number(
    session: AsyncSession, agent_number: str, tenant_uuids: list[str] | None = None
) -> AgentLoginStatus | None:
    """Get login status of an agent by number.

    Args:
        session: Database session
        agent_number: Agent number
        tenant_uuids: Optional tenant identifiers to filter by

    Returns:
        Agent login status or None if not found

    """
    stmt = (
        select(AgentLoginStatus)
        .outerjoin(AgentFeatures, AgentFeatures.id == AgentLoginStatus.agent_id)
        .filter(AgentLoginStatus.agent_number == agent_number)
    )
    if tenant_uuids is not None:
        stmt = stmt.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    return result.scalars().first()


async def _get_login_status_by_user(
    session: AsyncSession, user_uuid: str, tenant_uuids: list[str] | None = None
) -> AgentLoginStatus | None:
    """Get login status of an agent by user UUID.

    Args:
        session: Database session
        user_uuid: User identifier
        tenant_uuids: Optional tenant identifiers to filter by

    Returns:
        Agent login status or None if not found

    """
    stmt = (
        select(AgentLoginStatus)
        .outerjoin(AgentFeatures, AgentFeatures.id == AgentLoginStatus.agent_id)
        .join(UserFeatures, AgentFeatures.id == UserFeatures.agentid)
        .filter(UserFeatures.uuid == user_uuid)
    )
    if tenant_uuids is not None:
        stmt = stmt.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    return result.scalars().first()


async def _get_queues_for_agent(session: AsyncSession, agent_id: int) -> list[Queue]:
    """Get queues for an agent.

    Args:
        session: Database session
        agent_id: Agent identifier

    Returns:
        List of queues the agent belongs to

    """
    stmt = select(
        AgentMembershipStatus.queue_id.label("queue_id"),
        AgentMembershipStatus.queue_name.label("queue_name"),
        AgentMembershipStatus.penalty.label("penalty"),
    ).filter(AgentMembershipStatus.agent_id == agent_id)

    result = await session.execute(stmt)
    return [Queue(q.queue_id, q.queue_name, q.penalty) for q in result]


@async_daosession
async def get_extension_from_agent_id(
    session: AsyncSession, agent_id: int
) -> tuple[str, str]:
    """Get extension and context from agent ID.

    Args:
        session: Database session
        agent_id: Agent identifier

    Returns:
        Tuple of (extension, context)

    Raises:
        LookupError: If the agent is not logged in

    """
    stmt = select(AgentLoginStatus.extension, AgentLoginStatus.context).filter(
        AgentLoginStatus.agent_id == agent_id
    )

    result = await session.execute(stmt)
    login_status_row = result.first()

    if not login_status_row:
        error_msg = f"Agent with id {agent_id} is not logged in"
        raise LookupError(error_msg)

    return login_status_row.extension, login_status_row.context


@async_daosession
async def get_agent_id_from_extension(
    session: AsyncSession, extension: str, context: str
) -> int:
    """Get agent ID from extension and context.

    Args:
        session: Database session
        extension: Extension
        context: Context

    Returns:
        Agent identifier

    Raises:
        LookupError: If no agent is logged in on the specified extension

    """
    stmt = (
        select(AgentLoginStatus)
        .filter(AgentLoginStatus.extension == extension)
        .filter(AgentLoginStatus.context == context)
    )

    result = await session.execute(stmt)
    login_status = result.scalars().first()

    if not login_status:
        error_msg = f"No agent logged onto extension {extension}@{context}"
        raise LookupError(error_msg)

    return login_status.agent_id


@async_daosession
async def get_statuses(
    session: AsyncSession, tenant_uuids: list[str] | None = None
) -> Sequence[Any]:
    """Get statuses of all agents.

    Args:
        session: Database session
        tenant_uuids: Optional tenant identifiers to filter by

    Returns:
        Sequence of agent statuses

    """
    # Using case with values in SQLAlchemy 2.x
    case_expr = case((AgentLoginStatus.agent_id.is_(None), false()), else_=true())

    stmt = select(
        AgentFeatures.id.label("agent_id"),
        AgentFeatures.tenant_uuid.label("tenant_uuid"),
        AgentFeatures.number.label("agent_number"),
        AgentLoginStatus.extension.label("extension"),
        AgentLoginStatus.context.label("context"),
        AgentLoginStatus.state_interface.label("state_interface"),
        AgentLoginStatus.paused.label("paused"),
        AgentLoginStatus.paused_reason.label("paused_reason"),
        case_expr.label("logged"),
    ).outerjoin(AgentLoginStatus, AgentFeatures.id == AgentLoginStatus.agent_id)

    if tenant_uuids is not None:
        stmt = stmt.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    return result.all()


@async_daosession
async def get_statuses_for_queue(
    session: AsyncSession, queue_id: int
) -> list[AgentStatus]:
    """Get statuses of all agents in a queue.

    Args:
        session: Database session
        queue_id: Queue identifier

    Returns:
        List of agent statuses

    """
    subquery = (
        select(QueueMember.userid)
        .filter(QueueFeatures.name == QueueMember.queue_name)
        .filter(QueueFeatures.id == queue_id)
        .filter(QueueMember.usertype == "agent")
        .scalar_subquery()
    )

    stmt = select(AgentLoginStatus).filter(AgentLoginStatus.agent_id.in_(subquery))
    result = await session.execute(stmt)
    agent_statuses = result.scalars().all()

    return [_to_agent_status(q, None) for q in agent_statuses]


@async_daosession
async def get_statuses_to_add_to_queue(
    session: AsyncSession, queue_id: int
) -> list[AgentStatus]:
    """Get statuses of agents to add to a queue.

    Args:
        session: Database session
        queue_id: Queue identifier

    Returns:
        List of agent statuses

    """
    # In SQLAlchemy 2.x, we need to use except_ instead of except
    q1 = (
        select(QueueMember.userid)
        .filter(QueueFeatures.name == QueueMember.queue_name)
        .filter(QueueFeatures.id == queue_id)
        .filter(QueueMember.usertype == "agent")
    )

    q2 = select(AgentMembershipStatus.agent_id).filter(
        AgentMembershipStatus.queue_id == queue_id
    )

    # Create a combined query with except_
    agent_ids_to_add = q1.except_(q2).scalar_subquery()

    stmt = select(AgentLoginStatus).filter(
        AgentLoginStatus.agent_id.in_(agent_ids_to_add)
    )
    result = await session.execute(stmt)
    agent_statuses = result.scalars().all()

    return [_to_agent_status(q, None) for q in agent_statuses]


@async_daosession
async def get_statuses_to_remove_from_queue(
    session: AsyncSession, queue_id: int
) -> list[AgentStatus]:
    """Get statuses of agents to remove from a queue.

    Args:
        session: Database session
        queue_id: Queue identifier

    Returns:
        List of agent statuses

    """
    q1 = select(AgentMembershipStatus.agent_id).filter(
        AgentMembershipStatus.queue_id == queue_id
    )

    q2 = (
        select(QueueMember.userid)
        .filter(QueueFeatures.name == QueueMember.queue_name)
        .filter(QueueFeatures.id == queue_id)
        .filter(QueueMember.usertype == "agent")
    )

    # Create a combined query with except_
    agent_ids_to_remove = q1.except_(q2).scalar_subquery()

    stmt = select(AgentLoginStatus).filter(
        AgentLoginStatus.agent_id.in_(agent_ids_to_remove)
    )
    result = await session.execute(stmt)
    agent_statuses = result.scalars().all()

    return [_to_agent_status(q, None) for q in agent_statuses]


@async_daosession
async def get_logged_agent_ids(
    session: AsyncSession, tenant_uuids: list[str] | None = None
) -> list[int]:
    """Get IDs of logged in agents.

    Args:
        session: Database session
        tenant_uuids: Optional tenant identifiers to filter by

    Returns:
        List of agent identifiers

    """
    stmt = select(AgentLoginStatus.agent_id, AgentFeatures.tenant_uuid).outerjoin(
        AgentFeatures, AgentFeatures.id == AgentLoginStatus.agent_id
    )

    if tenant_uuids is not None:
        stmt = stmt.filter(AgentFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    return [q.agent_id for q in result]


def _to_agent_status(
    agent_login_status: AgentLoginStatus, queues: list[Queue] | None
) -> AgentStatus:
    """Convert agent login status to agent status.

    Args:
        agent_login_status: Agent login status
        queues: List of queues the agent belongs to

    Returns:
        Agent status

    """
    agent = agent_login_status.agent
    user_ids = [user.id for user in agent.users] if agent else []

    # Cast DateTime to datetime to fix type incompatibility
    login_at = cast(datetime, agent_login_status.login_at)

    return AgentStatus(
        agent_login_status.agent_id,
        agent_login_status.agent_number,
        agent_login_status.extension,
        agent_login_status.context,
        agent_login_status.interface,
        agent_login_status.state_interface,
        login_at,
        agent_login_status.paused,
        agent_login_status.paused_reason,
        queues,
        user_ids,
    )


@async_daosession
async def is_extension_in_use(
    session: AsyncSession, extension: str, context: str
) -> bool:
    """Check if an extension is in use.

    Args:
        session: Database session
        extension: Extension
        context: Context

    Returns:
        True if the extension is in use, False otherwise

    """
    stmt = (
        select(AgentLoginStatus)
        .filter(AgentLoginStatus.extension == extension)
        .filter(AgentLoginStatus.context == context)
    )

    result = await session.execute(stmt)
    count = len(result.scalars().all())

    return count > 0


# Create dataclass for input parameters to resolve too many arguments issue
class AgentLoginData:
    """Data for logging in an agent.

    Attributes:
        agent_id: Agent identifier
        agent_number: Agent number
        extension: Extension
        context: Context
        interface: Interface
        state_interface: State interface

    """

    def __init__(  # noqa: PLR0913
        self,
        agent_id: int,
        agent_number: str,
        extension: str,
        context: str,
        interface: str,
        state_interface: str,
    ) -> None:
        """Initialize agent login data.

        Args:
            agent_id: Agent identifier
            agent_number: Agent number
            extension: Extension
            context: Context
            interface: Interface
            state_interface: State interface

        """
        self.agent_id = agent_id
        self.agent_number = agent_number
        self.extension = extension
        self.context = context
        self.interface = interface
        self.state_interface = state_interface


@async_daosession
async def log_in_agent(  # noqa: PLR0913
    session: AsyncSession,
    agent_id: int,
    agent_number: str,
    extension: str,
    context: str,
    interface: str,
    state_interface: str,
) -> None:
    """Log in an agent.

    Args:
        session: Database session
        agent_id: Agent identifier
        agent_number: Agent number
        extension: Extension
        context: Context
        interface: Interface
        state_interface: State interface

    """
    # Create a wrapper function that takes fewer parameters
    data = AgentLoginData(
        agent_id=agent_id,
        agent_number=agent_number,
        extension=extension,
        context=context,
        interface=interface,
        state_interface=state_interface,
    )
    await _log_in_agent_impl(session, data)


async def _log_in_agent_impl(session: AsyncSession, data: AgentLoginData) -> None:
    """Implement log_in_agent with fewer parameters.

    Args:
        session: Database session
        data: Agent login data

    """
    agent = AgentLoginStatus()
    agent.agent_id = data.agent_id
    agent.agent_number = data.agent_number
    agent.extension = data.extension
    agent.context = data.context
    agent.interface = data.interface
    agent.state_interface = data.state_interface
    agent.paused = False

    await _add_agent(session, agent)


async def _add_agent(session: AsyncSession, agent: AgentLoginStatus) -> None:
    """Add an agent to the database.

    Args:
        session: Database session
        agent: Agent login status to add

    """
    async with async_flush_session(session):
        session.add(agent)


@async_daosession
async def log_off_agent(session: AsyncSession, agent_id: int) -> None:
    """Log off an agent.

    Args:
        session: Database session
        agent_id: Agent identifier

    """
    stmt = select(AgentLoginStatus).filter(AgentLoginStatus.agent_id == agent_id)

    result = await session.execute(stmt)
    agent_login_statuses = result.scalars().all()

    for agent_login_status in agent_login_statuses:
        await session.delete(agent_login_status)


@async_daosession
async def add_agent_to_queues(
    session: AsyncSession, agent_id: int, queues: list[Queue]
) -> None:
    """Add an agent to queues.

    Args:
        session: Database session
        agent_id: Agent identifier
        queues: List of queues to add the agent to

    """
    for queue in queues:
        agent_membership_status = AgentMembershipStatus(
            agent_id=agent_id,
            queue_id=queue.id,
            queue_name=queue.name,
            penalty=queue.penalty,
        )
        session.add(agent_membership_status)


@async_daosession
async def remove_agent_from_queues(
    session: AsyncSession, agent_id: int, queue_ids: list[int]
) -> None:
    """Remove an agent from queues.

    Args:
        session: Database session
        agent_id: Agent identifier
        queue_ids: List of queue identifiers to remove the agent from

    """
    stmt = (
        select(AgentMembershipStatus)
        .filter(AgentMembershipStatus.agent_id == agent_id)
        .filter(AgentMembershipStatus.queue_id.in_(queue_ids))
    )

    result = await session.execute(stmt)
    memberships = result.scalars().all()

    for membership in memberships:
        await session.delete(membership)


@async_daosession
async def remove_agent_from_all_queues(session: AsyncSession, agent_id: int) -> None:
    """Remove an agent from all queues.

    Args:
        session: Database session
        agent_id: Agent identifier

    """
    stmt = select(AgentMembershipStatus).filter(
        AgentMembershipStatus.agent_id == agent_id
    )

    result = await session.execute(stmt)
    memberships = result.scalars().all()

    for membership in memberships:
        await session.delete(membership)


@async_daosession
async def remove_all_agents_from_queue(session: AsyncSession, queue_id: int) -> None:
    """Remove all agents from a queue.

    Args:
        session: Database session
        queue_id: Queue identifier

    """
    stmt = select(AgentMembershipStatus).filter(
        AgentMembershipStatus.queue_id == queue_id
    )

    result = await session.execute(stmt)
    memberships = result.scalars().all()

    for membership in memberships:
        await session.delete(membership)


@async_daosession
async def update_penalty(
    session: AsyncSession, agent_id: int, queue_id: int, penalty: int
) -> None:
    """Update an agent's penalty in a queue.

    Args:
        session: Database session
        agent_id: Agent identifier
        queue_id: Queue identifier
        penalty: New penalty value

    """
    stmt = (
        select(AgentMembershipStatus)
        .filter(AgentMembershipStatus.queue_id == queue_id)
        .filter(AgentMembershipStatus.agent_id == agent_id)
    )

    result = await session.execute(stmt)
    membership = result.scalars().one()

    membership.penalty = penalty
    session.add(membership)


@async_daosession
async def update_pause_status(
    session: AsyncSession, agent_id: int, *, is_paused: bool, reason: str | None = None
) -> None:
    """Update an agent's pause status.

    Args:
        session: Database session
        agent_id: Agent identifier
        is_paused: Whether the agent is paused
        reason: Optional reason for the pause

    """
    stmt = select(AgentLoginStatus).filter(AgentLoginStatus.agent_id == agent_id)

    result = await session.execute(stmt)
    login_status = result.scalars().one()

    login_status.paused = is_paused
    login_status.paused_reason = reason
    session.add(login_status)
