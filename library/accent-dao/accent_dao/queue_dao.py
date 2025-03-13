# file: accent_dao/dao/queue_dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.helpers.db_manager import (
    async_daosession,
    cached_query,
    daosession,
    get_async_session,
)

# Set up logging
logger = logging.getLogger(__name__)


@daosession
def get(
    session: Session, queue_id: int, tenant_uuids: list[str] | None = None
) -> QueueFeatures:
    """Retrieve a queue by its ID and optional tenant UUIDs.

    Args:
        session: The database session.
        queue_id: The ID of the queue to retrieve.
        tenant_uuids: Optional list of tenant UUIDs to filter the queue.

    Returns:
        The queue features if found.

    Raises:
        LookupError: If no queue is found with the given ID.

    """
    # Updated for SQLAlchemy 2.x syntax
    stmt = select(QueueFeatures).where(QueueFeatures.id == queue_id)

    if tenant_uuids is not None:
        stmt = stmt.where(QueueFeatures.tenant_uuid.in_(tenant_uuids))

    result = session.execute(stmt).scalar_one_or_none()
    if result is None:
        logger.warning("Queue with id %s not found", queue_id)
        msg = "No such queue"
        raise LookupError(msg)

    logger.debug("Retrieved queue with id %s", queue_id)
    return result


@cached_query()
@daosession
def get_by_name(
    session: Session, name: str, tenant_uuids: list[str] | None = None
) -> QueueFeatures:
    """Retrieve a queue by its name and optional tenant UUIDs.

    Args:
        session: The database session.
        name: The name of the queue to retrieve.
        tenant_uuids: Optional list of tenant UUIDs to filter the queue.

    Returns:
        The queue features if found.

    Raises:
        LookupError: If no queue is found with the given name.

    """
    stmt = select(QueueFeatures).where(QueueFeatures.name == name)

    if tenant_uuids is not None:
        stmt = stmt.where(QueueFeatures.tenant_uuid.in_(tenant_uuids))

    result = session.execute(stmt).scalar_one_or_none()
    if result is None:
        logger.warning("Queue with name %s not found", name)
        msg = "No such queue"
        raise LookupError(msg)

    logger.debug("Retrieved queue with name %s", name)
    return result


@async_daosession
async def async_get(
    session: AsyncSession, queue_id: int, tenant_uuids: list[str] | None = None
) -> QueueFeatures:
    """Retrieve a queue by its ID and optional tenant UUIDs asynchronously.

    Args:
        session: The async database session.
        queue_id: The ID of the queue to retrieve.
        tenant_uuids: Optional list of tenant UUIDs to filter the queue.

    Returns:
        The queue features if found.

    Raises:
        LookupError: If no queue is found with the given ID.

    """
    # SQLAlchemy 2.x async syntax
    stmt = select(QueueFeatures).where(QueueFeatures.id == queue_id)

    if tenant_uuids is not None:
        stmt = stmt.where(QueueFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    queue = result.scalar_one_or_none()

    if queue is None:
        logger.warning("Queue with id %s not found", queue_id)
        msg = "No such queue"
        raise LookupError(msg)

    logger.debug("Retrieved queue with id %s", queue_id)
    return queue


@cached_query()
@async_daosession
async def async_get_by_name(
    session: AsyncSession, name: str, tenant_uuids: list[str] | None = None
) -> QueueFeatures:
    """Retrieve a queue by its name and optional tenant UUIDs asynchronously.

    Args:
        session: The async database session.
        name: The name of the queue to retrieve.
        tenant_uuids: Optional list of tenant UUIDs to filter the queue.

    Returns:
        The queue features if found.

    Raises:
        LookupError: If no queue is found with the given name.

    """
    stmt = select(QueueFeatures).where(QueueFeatures.name == name)

    if tenant_uuids is not None:
        stmt = stmt.where(QueueFeatures.tenant_uuid.in_(tenant_uuids))

    result = await session.execute(stmt)
    queue = result.scalar_one_or_none()

    if queue is None:
        logger.warning("Queue with name %s not found", name)
        msg = "No such queue"
        raise LookupError(msg)

    logger.debug("Retrieved queue with name %s", name)
    return queue


async def async_get_all(
    tenant_uuids: list[str] | str | None = None,
) -> list[QueueFeatures]:
    """Retrieve all queues filtered by optional tenant UUIDs asynchronously.

    Args:
        tenant_uuids: Optional list of tenant UUIDs or single UUID to filter the queues.

    Returns:
        A list of queue features.

    """
    async with get_async_session() as session:
        stmt = select(QueueFeatures)

        if tenant_uuids is not None:
            if isinstance(tenant_uuids, str):
                stmt = stmt.where(QueueFeatures.tenant_uuid == tenant_uuids)
            else:
                stmt = stmt.where(QueueFeatures.tenant_uuid.in_(tenant_uuids))

        result = await session.execute(stmt)
        queues = result.scalars().all()

        logger.info("Retrieved %s queues", len(queues))
        return list(queues)


@daosession
def get_all(
    session: Session, tenant_uuids: list[str] | str | None = None
) -> list[QueueFeatures]:
    """Retrieve all queues filtered by optional tenant UUIDs.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs or single UUID to filter the queues.

    Returns:
        A list of queue features.

    """
    stmt = select(QueueFeatures)

    if tenant_uuids is not None:
        if isinstance(tenant_uuids, str):
            stmt = stmt.where(QueueFeatures.tenant_uuid == tenant_uuids)
        else:
            stmt = stmt.where(QueueFeatures.tenant_uuid.in_(tenant_uuids))

    result = session.execute(stmt)
    queues = result.scalars().all()

    logger.info("Retrieved %s queues", len(queues))
    return list(queues)
