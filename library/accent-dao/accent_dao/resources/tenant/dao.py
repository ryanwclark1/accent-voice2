# file: accent_dao/resources/tenant/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.tenant import Tenant
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import TenantPersistor
from .search import tenant_search

logger = logging.getLogger(__name__)


@async_daosession
async def async_find(
    session: AsyncSession,
    resource_uuid: str,
    tenant_uuids: list[str] | None = None,
) -> Tenant | None:
    """Find a tenant by UUID.

    Args:
        session: The database session.
        resource_uuid: The UUID of the tenant.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The tenant if found, None otherwise.

    """
    return await TenantPersistor(session, tenant_search, tenant_uuids).find_by(
        {"uuid": resource_uuid}
    )


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Tenant]:
    """Find all tenants by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of tenant objects.

    """
    return await TenantPersistor(session, tenant_search, tenant_uuids).find_all_by(
        criteria
    )


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Tenant | None:
    """Find a tenant by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The tenant object if found, None otherwise.

    """
    return await TenantPersistor(session, tenant_search, tenant_uuids).find_by(criteria)


@async_daosession
async def async_get(
    session: AsyncSession, resource_uuid: str, tenant_uuids: list[str] | None = None
) -> Tenant:
    """Get a tenant by UUID.

    Args:
        session: The database session.
        resource_uuid: The UUID of the tenant.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The tenant object.

    """
    return await TenantPersistor(session, tenant_search, tenant_uuids).get_by(
        {"uuid": resource_uuid}
    )


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Tenant:
    """Get a tenant by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The tenant object.

    Raises:
        NotFoundError: If no tenant is found with the given criteria.

    """
    return await TenantPersistor(session, tenant_search, tenant_uuids).get_by(criteria)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for tenants.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and list of items.

    """
    return await TenantPersistor(session, tenant_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def async_edit(session: AsyncSession, tenant: Tenant) -> None:
    """Edit an existing tenant.

    Args:
        session: The database session.
        tenant: The tenant object to edit.

    """
    await TenantPersistor(session, tenant_search).edit(tenant)


@async_daosession
async def async_delete(session: AsyncSession, tenant: Tenant) -> None:
    """Delete a tenant.

    Args:
        session: The database session.
        tenant: The tenant object to delete.

    """
    await TenantPersistor(session, tenant_search).delete(tenant)
