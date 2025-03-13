# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.queue.persistor import QueuePersistor
from accent_dao.resources.queue.search import queue_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.alchemy.queuemember import QueueMember
    from accent_dao.alchemy.schedule import Schedule
    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for queues.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of queues.

    """
    return await QueuePersistor(session, queue_search, tenant_uuids).search(parameters)


@async_daosession
async def get(
    session: AsyncSession, queue_id: int, tenant_uuids: list[str] | None = None
) -> QueueFeatures:
    """Get a queue by ID.

    Args:
        session: The database session.
        queue_id: The ID of the queue.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The queue object.

    """
    return await QueuePersistor(session, queue_search, tenant_uuids).get_by(
        {"id": queue_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> QueueFeatures:
    """Get a queue by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The queue object.

    """
    return await QueuePersistor(session, queue_search, tenant_uuids).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession, queue_id: int, tenant_uuids: list[str] | None = None
) -> QueueFeatures | None:
    """Find a queue by ID.

    Args:
        session: The database session.
        queue_id: The ID of the queue.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The queue object or None if not found.

    """
    return await QueuePersistor(session, queue_search, tenant_uuids).find_by(
        {"id": queue_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> QueueFeatures | None:
    """Find a queue by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The queue object or None if not found.

    """
    return await QueuePersistor(session, queue_search, tenant_uuids).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[QueueFeatures]:
    """Find all queues by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of queue objects.

    """
    result: Sequence[QueueFeatures] = await QueuePersistor(
        session, queue_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, queue: QueueFeatures) -> QueueFeatures:
    """Create a new queue.

    Args:
        session: The database session.
        queue: The queue object to create.

    Returns:
        The created queue object.

    """
    return await QueuePersistor(session, queue_search).create(queue)


@async_daosession
async def edit(session: AsyncSession, queue: QueueFeatures) -> None:
    """Edit an existing queue.

    Args:
        session: The database session.
        queue: The queue object to edit.

    """
    await QueuePersistor(session, queue_search).edit(queue)


@async_daosession
async def delete(session: AsyncSession, queue: QueueFeatures) -> None:
    """Delete a queue.

    Args:
        session: The database session.
        queue: The queue object to delete.

    """
    await QueuePersistor(session, queue_search).delete(queue)


@async_daosession
async def associate_schedule(
    session: AsyncSession, queue: QueueFeatures, schedule: "Schedule"
) -> None:
    """Associate a schedule with a queue.

    Args:
        session: The database session.
        queue: The queue object.
        schedule: The schedule object to associate.

    """
    await QueuePersistor(session, queue_search).associate_schedule(queue, schedule)


@async_daosession
async def dissociate_schedule(
    session: AsyncSession, queue: QueueFeatures, schedule: "Schedule"
) -> None:
    """Dissociate a schedule from a queue.

    Args:
        session: The database session.
        queue: The queue object.
        schedule: The schedule object to dissociate.

    """
    await QueuePersistor(session, queue_search).dissociate_schedule(queue, schedule)


@async_daosession
async def associate_member_user(
    session: AsyncSession, queue: QueueFeatures, member: "QueueMember"
) -> None:
    """Associate a user member with a queue.

    Args:
        session: The database session.
        queue: The queue object.
        member: The user member object to associate.

    """
    await QueuePersistor(session, queue_search).associate_member_user(queue, member)


@async_daosession
async def dissociate_member_user(
    session: AsyncSession, queue: QueueFeatures, member: "QueueMember"
) -> None:
    """Dissociate a user member from a queue.

    Args:
        session: The database session.
        queue: The queue object.
        member: The user member object to dissociate.

    """
    await QueuePersistor(session, queue_search).dissociate_member_user(queue, member)


@async_daosession
async def associate_member_agent(
    session: AsyncSession, queue: QueueFeatures, member: "QueueMember"
) -> None:
    """Associate an agent member with a queue.

    Args:
        session: The database session.
        queue: The queue object.
        member: The agent member object to associate.

    """
    await QueuePersistor(session, queue_search).associate_member_agent(queue, member)


@async_daosession
async def dissociate_member_agent(
    session: AsyncSession, queue: QueueFeatures, member: "QueueMember"
) -> None:
    """Dissociate an agent member from a queue.

    Args:
        session: The database session.
        queue: The queue object.
        member: The agent member object to dissociate.

    """
    await QueuePersistor(session, queue_search).dissociate_member_agent(queue, member)
