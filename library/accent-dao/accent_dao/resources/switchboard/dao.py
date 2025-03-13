# file: accent_dao/resources/switchboard/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.switchboard import Switchboard
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import SwitchboardPersistor
from .search import switchboard_search

logger = logging.getLogger(__name__)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for switchboards.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.

    """
    return await SwitchboardPersistor(session, switchboard_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def async_get(
    session: AsyncSession, switchboard_uuid: str, tenant_uuids: list[str] | None = None
) -> Switchboard:
    """Get a switchboard by UUID.

    Args:
        session: The database session.
        switchboard_uuid: The UUID of the switchboard.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The switchboard.

    """
    return await SwitchboardPersistor(session, switchboard_search, tenant_uuids).get_by(
        {"uuid": switchboard_uuid}
    )


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Switchboard:
    """Get a switchboard by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The switchboard.

    Raises:
        NotFoundError: If no switchboard is found with the given criteria.

    """
    return await SwitchboardPersistor(session, switchboard_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Switchboard | None:
    """Find a switchboard by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The switchboard if found, None otherwise.

    """
    return await SwitchboardPersistor(
        session, switchboard_search, tenant_uuids
    ).find_by(criteria)


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Switchboard]:
    """Find all switchboards by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of switchboards.

    """
    return await SwitchboardPersistor(
        session, switchboard_search, tenant_uuids
    ).find_all_by(criteria)


@async_daosession
async def async_create(session: AsyncSession, switchboard: Switchboard) -> Switchboard:
    """Create a new switchboard.

    Args:
        session: The database session.
        switchboard: The switchboard to create.

    Returns:
        The created switchboard.

    """
    return await SwitchboardPersistor(session, switchboard_search).create(switchboard)


@async_daosession
async def async_edit(session: AsyncSession, switchboard: Switchboard) -> None:
    """Edit an existing switchboard.

    Args:
        session: The database session.
        switchboard: The switchboard to edit.

    """
    await SwitchboardPersistor(session, switchboard_search).edit(switchboard)


@async_daosession
async def async_delete(session: AsyncSession, switchboard: Switchboard) -> None:
    """Delete a switchboard.

    Args:
        session: The database session.
        switchboard: The switchboard to delete.

    """
    await SwitchboardPersistor(session, switchboard_search).delete(switchboard)
