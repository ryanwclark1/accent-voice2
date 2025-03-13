# file: accent_dao/resources/meeting/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from accent_dao.helpers.db_manager import async_daosession

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from accent_dao.alchemy.meeting import Meeting
    from accent_dao.resources.utils.search import SearchResult

from .persistor import MeetingPersistor
from .search import meeting_search

# Configure logging
logger = logging.getLogger(__name__)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for meetings.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.

    """
    return await MeetingPersistor(session, meeting_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def async_get(
    session: AsyncSession, meeting_uuid: str, tenant_uuids: list[str] | None = None
) -> Meeting:
    """Get a meeting by UUID.

    Args:
        session: The database session.
        meeting_uuid: The UUID of the meeting.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The meeting object.

    Raises:
        NotFoundError: If no meeting is found with the given UUID.

    """
    return await MeetingPersistor(session, meeting_search, tenant_uuids).get_by(
        {"uuid": meeting_uuid}
    )


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Meeting:
    """Get a meeting by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The meeting object.

    Raises:
        NotFoundError: If no meeting is found with the given criteria.

    """
    return await MeetingPersistor(session, meeting_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Meeting | None:
    """Find a meeting by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The meeting object, or None if not found.

    """
    return await MeetingPersistor(session, meeting_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Meeting]:
    """Find all meetings by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of meeting objects.

    """
    return await MeetingPersistor(session, meeting_search, tenant_uuids).find_all_by(
        criteria
    )


@async_daosession
async def async_create(session: AsyncSession, meeting: Meeting) -> Meeting:
    """Create a new meeting.

    Args:
        session: The database session.
        meeting: The meeting object to create.

    Returns:
        The created meeting object.

    """
    return await MeetingPersistor(session, meeting_search).create(meeting)


@async_daosession
async def async_edit(session: AsyncSession, meeting: Meeting) -> None:
    """Edit an existing meeting.

    Args:
        session: The database session.
        meeting: The meeting object to edit.

    """
    await MeetingPersistor(session, meeting_search).edit(meeting)


@async_daosession
async def async_delete(session: AsyncSession, meeting: Meeting) -> None:
    """Delete a meeting.

    Args:
        session: The database session.
        meeting: The meeting object to delete.

    """
    await MeetingPersistor(session, meeting_search).delete(meeting)
