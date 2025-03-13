# file: accent_dao/resources/endpoint_sip/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

if TYPE_CHECKING:
    pass

from accent_dao.alchemy.endpoint_sip import EndpointSIP

from .persistor import SIPPersistor
from .search import sip_search

# Configure logging
logger = logging.getLogger(__name__)


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> EndpointSIP | None:
    """Find a SIP endpoint by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The SIP endpoint if found, None otherwise.

    """
    return await SIPPersistor(session, sip_search, tenant_uuids).find_by(criteria)


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[EndpointSIP]:
    """Find all SIP endpoints by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of SIP endpoint objects.

    """
    return await SIPPersistor(session, sip_search, tenant_uuids).find_all_by(criteria)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for SIP endpoints.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of items.

    """
    return await SIPPersistor(session, sip_search, tenant_uuids).search(parameters)


@async_daosession
async def async_get(
    session: AsyncSession, sip_uuid: str, tenant_uuids: list[str] | None = None
) -> EndpointSIP:
    """Get a SIP endpoint by UUID.

    Args:
        session: The database session.
        sip_uuid: The UUID of the SIP endpoint.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The SIP endpoint.

    """
    return await SIPPersistor(session, sip_search, tenant_uuids).get_by(
        {"uuid": sip_uuid}
    )


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> EndpointSIP:
    """Get a SIP endpoint by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The SIP endpoint.

    Raises:
        NotFoundError: If no SIP endpoint is found with the given criteria.

    """
    return await SIPPersistor(session, sip_search, tenant_uuids).get_by(criteria)


@async_daosession
async def async_create(session: AsyncSession, sip: EndpointSIP) -> EndpointSIP:
    """Create a new SIP endpoint.

    Args:
        session: The database session.
        sip: The SIP endpoint to create.

    Returns:
        The created SIP endpoint.

    """
    return await SIPPersistor(session, sip_search).create(sip)


@async_daosession
async def async_edit(session: AsyncSession, sip: EndpointSIP) -> None:
    """Edit an existing SIP endpoint.

    Args:
        session: The database session.
        sip: The SIP endpoint to edit.

    """
    await SIPPersistor(session, sip_search).edit(sip)


@async_daosession
async def async_delete(session: AsyncSession, sip: EndpointSIP) -> None:
    """Delete a SIP endpoint.

    Args:
        session: The database session.
        sip: The SIP endpoint to delete.

    """
    await SIPPersistor(session, sip_search).delete(sip)
