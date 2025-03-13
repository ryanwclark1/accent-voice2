# file: accent_dao/resources/conference/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from accent_dao.helpers.db_manager import async_daosession

from .persistor import ConferencePersistor
from .search import conference_search

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from accent_dao.alchemy.conference import Conference
    from accent_dao.resources.utils.search import SearchResult

# Configure logging
logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for conferences.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.

    """
    return await ConferencePersistor(session, conference_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def get(
    session: AsyncSession, conference_id: int, tenant_uuids: list[str] | None = None
) -> Conference:
    """Get a conference by ID.

    Args:
        session: The database session.
        conference_id: The ID of the conference.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        Conference: The conference.

    """
    return await ConferencePersistor(session, conference_search, tenant_uuids).get_by(
        {"id": conference_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Conference:
    """Get a conference by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        Conference: The conference.

    """
    return await ConferencePersistor(session, conference_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def find(
    session: AsyncSession,
    conference_id: int,
    tenant_uuids: list[str] | None = None,
) -> Conference | None:
    """Find a conference by ID.

    Args:
        session: The database session.
        conference_id: The ID of the conference.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        Conference | None: The conference, or None if not found.

    """
    return await ConferencePersistor(session, conference_search, tenant_uuids).find_by(
        {"id": conference_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Conference | None:
    """Find a conference by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        Conference | None: The conference, or None if not found.

    """
    return await ConferencePersistor(session, conference_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Conference]:
    """Find all conferences by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        list[Conference]: A list of conferences.

    """
    result = await ConferencePersistor(
        session, conference_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, conference: Conference) -> Conference:
    """Create a new conference.

    Args:
        session: The database session.
        conference: The conference to create.

    Returns:
        Conference: The created conference.

    """
    return await ConferencePersistor(session, conference_search).create(conference)


@async_daosession
async def edit(session: AsyncSession, conference: Conference) -> None:
    """Edit an existing conference.

    Args:
        session: The database session.
        conference: The conference to edit.

    """
    await ConferencePersistor(session, conference_search).edit(conference)


@async_daosession
async def delete(session: AsyncSession, conference: Conference) -> None:
    """Delete a conference.

    Args:
        session: The database session.
        conference: The conference to delete.

    """
    await ConferencePersistor(session, conference_search).delete(conference)
