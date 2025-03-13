# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.schedule import Schedule
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.schedule.persistor import SchedulePersistor
from accent_dao.resources.schedule.search import schedule_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for schedules.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of schedules.

    """
    return await SchedulePersistor(session, schedule_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def get(
    session: AsyncSession, schedule_id: int, tenant_uuids: list[str] | None = None
) -> Schedule:
    """Get a schedule by ID.

    Args:
        session: The database session.
        schedule_id: The ID of the schedule.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The schedule object.

    """
    return await SchedulePersistor(session, schedule_search, tenant_uuids).get_by(
        {"id": schedule_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Schedule:
    """Get a schedule by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The schedule object.

    """
    return await SchedulePersistor(session, schedule_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def find(
    session: AsyncSession, schedule_id: int, tenant_uuids: list[str] | None = None
) -> Schedule | None:
    """Find a schedule by ID.

    Args:
        session: The database session.
        schedule_id: The ID of the schedule.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The schedule object or None if not found.

    """
    return await SchedulePersistor(session, schedule_search, tenant_uuids).find_by(
        {"id": schedule_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Schedule | None:
    """Find a schedule by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The schedule object or None if not found.

    """
    return await SchedulePersistor(session, schedule_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Schedule]:
    """Find all schedules by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of schedule objects.

    """
    result: Sequence[Schedule] = await SchedulePersistor(
        session, schedule_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, schedule: Schedule) -> Schedule:
    """Create a new schedule.

    Args:
        session: The database session.
        schedule: The schedule object to create.

    Returns:
        The created schedule object.

    """
    return await SchedulePersistor(session, schedule_search).create(schedule)


@async_daosession
async def edit(session: AsyncSession, schedule: Schedule) -> None:
    """Edit an existing schedule.

    Args:
        session: The database session.
        schedule: The schedule object to edit.

    """
    await SchedulePersistor(session, schedule_search).edit(schedule)


@async_daosession
async def delete(session: AsyncSession, schedule: Schedule) -> None:
    """Delete a schedule.

    Args:
        session: The database session.
        schedule: The schedule object to delete.

    """
    await SchedulePersistor(session, schedule_search).delete(schedule)
