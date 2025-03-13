# file: accent_dao/resources/endpoint_sccp/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.sccpline import SCCPLine
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import SCCPPersistor
from .search import sccp_search

# Configure logging
logger = logging.getLogger(__name__)


@async_daosession
async def async_get(
    session: AsyncSession, sccp_id: int, tenant_uuids: list[str] | None = None
) -> SCCPLine:
    """Get an SCCP endpoint by ID.

    Args:
        session: The database session.
        sccp_id: The ID of the SCCP endpoint.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The SCCP endpoint.

    """
    return await SCCPPersistor(session, sccp_search, tenant_uuids).get_by(
        {"id": sccp_id}
    )


@async_daosession
async def async_find(
    session: AsyncSession, sccp_id: int, tenant_uuids: list[str] | None = None
) -> SCCPLine | None:
    """Find an SCCP endpoint by ID.

    Args:
        session: The database session.
        sccp_id: The ID of the SCCP endpoint.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The SCCP endpoint if found, None otherwise.

    """
    return await SCCPPersistor(session, sccp_search, tenant_uuids).find_by(
        {"id": sccp_id}
    )


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for SCCP endpoints.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of items.

    """
    return await SCCPPersistor(session, sccp_search, tenant_uuids).search(parameters)


@async_daosession
async def async_create(session: AsyncSession, sccp: SCCPLine) -> SCCPLine:
    """Create a new SCCP endpoint.

    Args:
        session: The database session.
        sccp: The SCCP endpoint to create.

    Returns:
        The created SCCP endpoint.

    """
    return await SCCPPersistor(session, sccp_search).create(sccp)


@async_daosession
async def async_edit(session: AsyncSession, sccp: SCCPLine) -> None:
    """Edit an existing SCCP endpoint.

    Args:
        session: The database session.
        sccp: The SCCP endpoint to edit.

    """
    await SCCPPersistor(session, sccp_search).edit(sccp)


@async_daosession
async def async_delete(session: AsyncSession, sccp: SCCPLine) -> None:
    """Delete an SCCP endpoint.

    Args:
        session: The database session.
        sccp: The SCCP endpoint to delete.

    """
    await SCCPPersistor(session, sccp_search).delete(sccp)


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> SCCPLine | None:
    """Find a SCCP endpoint by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The SCCP endpoint if found, None otherwise.

    """
    return await SCCPPersistor(session, sccp_search, tenant_uuids).find_by(criteria)


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> SCCPLine:
    """Get a SCCP endpoint by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The SCCP endpoint object.

    Raises:
        NotFoundError: If no endpoint is found with the given criteria.

    """
    return await SCCPPersistor(session, sccp_search, tenant_uuids).get_by(criteria)


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[SCCPLine]:
    """Find all SCCP endpoints by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of SCCP endpoint objects.

    """
    return await SCCPPersistor(session, sccp_search, tenant_uuids).find_all_by(criteria)
