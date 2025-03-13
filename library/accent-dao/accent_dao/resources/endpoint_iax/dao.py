# file: accent_dao/resources/endpoint_iax/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.useriax import UserIAX as IAXEndpoint
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import IAXPersistor
from .search import iax_search

logger = logging.getLogger(__name__)


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> IAXEndpoint | None:
    """Find an IAX endpoint by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The IAX endpoint if found, None otherwise.

    """
    return await IAXPersistor(session, iax_search, tenant_uuids).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[IAXEndpoint]:
    """Find all IAX endpoints by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of IAXEndpoint objects.

    """
    return await IAXPersistor(session, iax_search, tenant_uuids).find_all_by(criteria)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for IAX endpoints.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of items.

    """
    return await IAXPersistor(session, iax_search, tenant_uuids).search(parameters)


@async_daosession
async def get(
    session: AsyncSession, iax_id: int, tenant_uuids: list[str] | None = None
) -> IAXEndpoint:
    """Get an IAX endpoint by ID.

    Args:
        session: The database session.
        iax_id: The ID of the IAX endpoint.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The IAX endpoint.

    """
    return await IAXPersistor(session, iax_search, tenant_uuids).get_by({"id": iax_id})


@async_daosession
async def create(session: AsyncSession, iax: IAXEndpoint) -> IAXEndpoint:
    """Create a new IAX endpoint.

    Args:
        session: The database session.
        iax: The IAX endpoint to create.

    Returns:
        The created IAX endpoint.

    """
    return await IAXPersistor(session, iax_search).create(iax)


@async_daosession
async def edit(session: AsyncSession, iax: IAXEndpoint) -> None:
    """Edit an existing IAX endpoint.

    Args:
        session: The database session.
        iax: The IAX endpoint to edit.

    """
    await IAXPersistor(session, iax_search).edit(iax)


@async_daosession
async def delete(session: AsyncSession, iax: IAXEndpoint) -> None:
    """Delete an IAX endpoint.

    Args:
        session: The database session.
        iax: The IAX endpoint to delete.

    """
    await IAXPersistor(session, iax_search).delete(iax)
