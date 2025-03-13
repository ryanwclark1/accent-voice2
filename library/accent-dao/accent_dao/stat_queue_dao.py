# file: accent_dao/alchemy/stat_queue_dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

"""Data access operations for StatQueue entities."""

import logging
from typing import Any

from sqlalchemy import delete, distinct, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.stat_queue import StatQueue
from accent_dao.helpers.db_manager import async_daosession

logger = logging.getLogger(__name__)



@async_daosession
async def get(session: AsyncSession, queue_id: int) -> StatQueue:
    """Retrieve a StatQueue by ID asynchronously.

    Args:
        session: The async database session
        queue_id: The ID of the queue to retrieve

    Returns:
        The StatQueue object

    Raises:
        IndexError: If no queue with the given ID exists

    """
    result = await session.execute(select(StatQueue).filter(StatQueue.id == queue_id))
    queue = result.scalar_one_or_none()

    if queue is None:
        logger.error("StatQueue with ID %s not found", queue_id)
        msg = f"No StatQueue found with ID {queue_id}"
        raise IndexError(msg)

    return queue



@async_daosession
async def _get(session: AsyncSession, queue_id: int) -> StatQueue:
    """Retrieve a StatQueue by ID asynchronously (internal version).

    Args:
        session: The async database session
        queue_id: The ID of the queue to retrieve

    Returns:
        The StatQueue object

    Raises:
        IndexError: If no queue with the given ID exists

    """
    result = await session.execute(select(StatQueue).filter(StatQueue.id == queue_id))
    queue = result.scalar_one_or_none()

    if queue is None:
        logger.error("StatQueue with ID %s not found", queue_id)
        msg = f"No StatQueue found with ID {queue_id}"
        raise IndexError(msg)

    return queue


@async_daosession
async def id_from_name(session: AsyncSession, queue_name: str) -> int:
    """Get a queue ID from its name asynchronously.

    Args:
        session: The async database session
        queue_name: The name of the queue

    Returns:
        The ID of the queue

    Raises:
        LookupError: If no queue with the given name exists

    """
    result = await session.execute(
        select(StatQueue).filter(StatQueue.name == queue_name)
    )
    queues = result.scalars().all()

    if not queues:
        logger.error("No queue found with name %s", queue_name)
        msg = "No such queue"
        raise LookupError(msg)

    return queues[0].id


async def insert_if_missing(
    session: AsyncSession,
    queuelog_queues: list[str],
    confd_queues: list[dict[str, Any]],
    master_tenant: str,
) -> None:
    """Insert queues that are missing and handle renamed/deleted queues asynchronously.

    Args:
        session: The async database session
        queuelog_queues: List of queue names from queuelog
        confd_queues: List of queue dictionaries from ConFD
        master_tenant: The UUID of the master tenant

    """
    confd_queues_by_name = {queue["name"]: queue for queue in confd_queues}
    await _mark_recreated_queues_with_same_name_as_deleted(
        session, confd_queues_by_name
    )
    await _mark_non_confd_queues_as_deleted(session, confd_queues)
    await _create_missing_queues(
        session, queuelog_queues, confd_queues_by_name, master_tenant
    )
    await _rename_deleted_queues_with_duplicate_name(
        session, confd_queues_by_name
    )


async def _mark_recreated_queues_with_same_name_as_deleted(
    session: AsyncSession, confd_queues_by_name: dict[str, dict[str, Any]]
) -> None:
    """Mark queues with same name but different ID as deleted asynchronously.

    Args:
        session: The async database session
        confd_queues_by_name: Dictionary of queue data by name

    """
    result = await session.execute(
        select(StatQueue).filter(StatQueue.deleted.is_(False))
    )
    db_queue_query = result.scalars().all()

    db_queues_by_name = {queue.name: queue for queue in db_queue_query}

    confd_queue_names = set(list(confd_queues_by_name.keys()))
    db_queue_names = set(list(db_queues_by_name.keys()))

    not_missing_queues = confd_queue_names.intersection(db_queue_names)
    for queue_name in not_missing_queues:
        confd_queue = confd_queues_by_name[queue_name]
        db_queue = db_queues_by_name[queue_name]
        if db_queue.queue_id != confd_queue["id"]:
            db_queue.deleted = True
            await session.flush()


async def _mark_non_confd_queues_as_deleted(
    session: AsyncSession, confd_queues: list[dict[str, Any]]
) -> None:
    """Mark queues not in ConFD as deleted asynchronously.

    Args:
        session: The async database session
        confd_queues: List of queue dictionaries from ConFD

    """
    active_queue_ids = {queue["id"] for queue in confd_queues}

    result = await session.execute(select(distinct(StatQueue.queue_id)))
    all_queue_ids = {r[0] for r in result}

    deleted_queues = [
        queue for queue in list(all_queue_ids - active_queue_ids) if queue
    ]

    await session.execute(
        update(StatQueue)
        .where(
            or_(
                StatQueue.queue_id.in_(deleted_queues),
                StatQueue.queue_id.is_(None),
            )
        )
        .values(deleted=True)
    )

    await session.flush()


async def _create_missing_queues(
    session: AsyncSession,
    queuelog_queues: list[str],
    confd_queues_by_name: dict[str, dict[str, Any]],
    master_tenant: str,
) -> None:
    """Create queues that are missing from the database asynchronously.

    Args:
        session: The async database session
        queuelog_queues: List of queue names from queuelog
        confd_queues_by_name: Dictionary of queue data by name
        master_tenant: The UUID of the master tenant

    """
    new_queue_names = set(confd_queues_by_name.keys())

    result = await session.execute(
        select(StatQueue).filter(StatQueue.deleted.is_(False))
    )
    db_queue_query = result.scalars().all()

    old_queue_names = {queue.name for queue in db_queue_query}
    missing_queues = list(new_queue_names - old_queue_names)

    for queue_name in missing_queues:
        queue = confd_queues_by_name[queue_name]
        new_queue = StatQueue()
        new_queue.name = queue_name
        new_queue.tenant_uuid = queue["tenant_uuid"]
        new_queue.queue_id = queue["id"]
        new_queue.deleted = False
        session.add(new_queue)
        await session.flush()

    result = await session.execute(
        select(StatQueue).filter(StatQueue.deleted.is_(True))
    )
    db_queue_query = result.scalars().all()

    old_queue_names = {queue.name for queue in db_queue_query}
    missing_queues = list(set(queuelog_queues) - old_queue_names - new_queue_names)

    for queue_name in missing_queues:
        new_queue = StatQueue()
        new_queue.name = queue_name
        new_queue.tenant_uuid = master_tenant
        new_queue.deleted = True
        session.add(new_queue)
        await session.flush()


async def _rename_deleted_queues_with_duplicate_name(
    session: AsyncSession, confd_queues_by_name: dict[str, dict[str, Any]]
) -> None:
    """Rename deleted queues with duplicate names to avoid conflicts asynchronously.

    Args:
        session: The async database session
        confd_queues_by_name: Dictionary of queue data by name

    """
    result = await session.execute(
        select(StatQueue).filter(StatQueue.deleted.is_(True))
    )
    db_queue_query = result.scalars().all()

    for queue in db_queue_query:
        if queue.name in confd_queues_by_name:
            queue.name = await _find_next_available_name(session, queue.name)
            await session.flush()


async def _find_next_available_name(session: AsyncSession, name: str) -> str:
    """Find the next available queue name that doesn't conflict asynchronously.

    Args:
        session: The async database session
        name: The base name to check

    Returns:
        A non-conflicting queue name

    """
    result = await session.execute(select(StatQueue).filter(StatQueue.name == name))
    query = result.first()

    if query:
        next_name = f"{name}_"
        return await _find_next_available_name(session, next_name)

    return name


@async_daosession
async def clean_table(session: AsyncSession) -> None:
    """Remove all entries from the StatQueue table asynchronously.

    Args:
        session: The async database session

    """
    logger.warning("Cleaning all data from stat_queue table")
    await session.execute(delete(StatQueue))
    await session.flush()
