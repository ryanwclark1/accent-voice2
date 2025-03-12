# file: accent_dao/resources/application/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.application import Application
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import ApplicationPersistor
from .search import application_search

if TYPE_CHECKING:
    from collections.abc import Sequence




@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for applications.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.

    """
    return await ApplicationPersistor(session, application_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def get(
    session: AsyncSession,
    application_uuid: str,
    tenant_uuids: list[str] | None = None,
) -> Application:
    """Get an application by UUID.

    Args:
        session: The database session.
        application_uuid: The UUID of the application.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        Application: The application.

    """
    return await ApplicationPersistor(session, application_search, tenant_uuids).get_by(
        {"uuid": application_uuid}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Application:
    """Get an application by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        Application: The application.

    """
    return await ApplicationPersistor(session, application_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def find(
    session: AsyncSession,
    application_uuid: str,
    tenant_uuids: list[str] | None = None,
) -> Application | None:
    """Find an application by UUID.

    Args:
        session: The database session.
        application_uuid: The UUID of the application.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        Application | None: The application, or None if not found.

    """
    return await ApplicationPersistor(
        session, application_search, tenant_uuids
    ).find_by({"uuid": application_uuid})


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Application | None:
    """Find an application by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        Application | None: The application, or None if not found.

    """
    return await ApplicationPersistor(
        session, application_search, tenant_uuids
    ).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Application]:
    """Find all applications by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        list[Application]: A list of applications.

    """
    result: Sequence[Application] = await ApplicationPersistor(
        session, application_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, application: Application) -> Application:
    """Create a new application.

    Args:
        session: The database session.
        application: The application to create.

    Returns:
        Application: The created application.

    """
    return await ApplicationPersistor(session, application_search).create(application)


@async_daosession
async def edit(session: AsyncSession, application: Application) -> None:
    """Edit an existing application.

    Args:
        session: The database session.
        application: The application to edit.

    """
    await ApplicationPersistor(session, application_search).edit(application)


@async_daosession
async def delete(session: AsyncSession, application: Application) -> None:
    """Delete an application.

    Args:
        session: The database session.
        application: The application to delete.

    """
    await ApplicationPersistor(session, application_search).delete(application)
