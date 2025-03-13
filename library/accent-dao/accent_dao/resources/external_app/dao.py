# file: accent_dao/resources/external_app/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.external_app import ExternalApp
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import ExternalAppPersistor
from .search import external_app_search

logger = logging.getLogger(__name__)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for external apps.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.

    """
    return await ExternalAppPersistor(
        session, external_app_search, tenant_uuids
    ).search(parameters)


@async_daosession
async def async_get(
    session: AsyncSession,
    external_app_name: str,
    tenant_uuids: list[str] | None = None,
) -> ExternalApp:
    """Get an external app by name.

    Args:
        session: The database session.
        external_app_name: The name of the external app.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The external app.

    """
    return await ExternalAppPersistor(
        session, external_app_search, tenant_uuids
    ).get_by({"name": external_app_name})


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> ExternalApp:
    """Get an external app by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The external app.

    Raises:
        NotFoundError: If no external app is found with the given criteria.

    """
    return await ExternalAppPersistor(
        session, external_app_search, tenant_uuids
    ).get_by(criteria)


@async_daosession
async def async_find(
    session: AsyncSession,
    external_app_name: str,
    tenant_uuids: list[str] | None = None,
) -> ExternalApp | None:
    """Find an external app by name.

    Args:
        session: The database session.
        external_app_name: The name of the external app.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The external app if found, None otherwise.

    """
    return await ExternalAppPersistor(
        session, external_app_search, tenant_uuids
    ).find_by({"name": external_app_name})


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> ExternalApp | None:
    """Find an external app by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The external app if found, None otherwise.

    """
    return await ExternalAppPersistor(
        session, external_app_search, tenant_uuids
    ).find_by(criteria)


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[ExternalApp]:
    """Find all external apps by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of external apps.

    """
    return await ExternalAppPersistor(
        session, external_app_search, tenant_uuids
    ).find_all_by(criteria)


@async_daosession
async def async_create(session: AsyncSession, external_app: ExternalApp) -> ExternalApp:
    """Create a new external app.

    Args:
        session: The database session.
        external_app: The external app to create.

    Returns:
        The created external app.

    """
    return await ExternalAppPersistor(session, external_app_search).create(external_app)


@async_daosession
async def async_edit(session: AsyncSession, external_app: ExternalApp) -> None:
    """Edit an existing external app.

    Args:
        session: The database session.
        external_app: The external app to edit.

    """
    await ExternalAppPersistor(session, external_app_search).edit(external_app)


@async_daosession
async def async_delete(session: AsyncSession, external_app: ExternalApp) -> None:
    """Delete an external app.

    Args:
        session: The database session.
        external_app: The external app to delete.

    """
    await ExternalAppPersistor(session, external_app_search).delete(external_app)
