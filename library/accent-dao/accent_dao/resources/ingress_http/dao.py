# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.ingress_http import IngressHTTP
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.ingress_http.persistor import IngressHTTPPersistor
from accent_dao.resources.ingress_http.search import http_ingress_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for HTTP ingress configurations.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of HTTP ingresses.

    """
    return await IngressHTTPPersistor(
        session, http_ingress_search, tenant_uuids
    ).search(parameters)


@async_daosession
async def get(
    session: AsyncSession,
    ingress_http_uuid: str,
    tenant_uuids: list[str] | None = None,
) -> IngressHTTP:
    """Get an HTTP ingress configuration by UUID.

    Args:
        session: The database session.
        ingress_http_uuid: The UUID of the HTTP ingress configuration.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The IngressHTTP object.

    """
    return await IngressHTTPPersistor(
        session, http_ingress_search, tenant_uuids
    ).get_by({"uuid": ingress_http_uuid})


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> IngressHTTP:
    """Get an HTTP ingress configuration by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The IngressHTTP object.

    """
    return await IngressHTTPPersistor(
        session, http_ingress_search, tenant_uuids
    ).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession,
    ingress_http_uuid: str,
    tenant_uuids: list[str] | None = None,
) -> IngressHTTP | None:
    """Find an HTTP ingress configuration by UUID.

    Args:
        session: The database session.
        ingress_http_uuid: The UUID of the HTTP ingress configuration.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The IngressHTTP object or None if not found.

    """
    return await IngressHTTPPersistor(
        session, http_ingress_search, tenant_uuids
    ).find_by({"uuid": ingress_http_uuid})


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> IngressHTTP | None:
    """Find an HTTP ingress configuration by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The IngressHTTP object or None if not found.

    """
    return await IngressHTTPPersistor(
        session, http_ingress_search, tenant_uuids
    ).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[IngressHTTP]:
    """Find all HTTP ingress configurations by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of IngressHTTP objects.

    """
    result: Sequence[IngressHTTP] = await IngressHTTPPersistor(
        session, http_ingress_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, ingress_http: IngressHTTP) -> IngressHTTP:
    """Create a new HTTP ingress configuration.

    Args:
        session: The database session.
        ingress_http: The IngressHTTP object to create.

    Returns:
        The created IngressHTTP object.

    """
    return await IngressHTTPPersistor(session, http_ingress_search).create(ingress_http)


@async_daosession
async def edit(session: AsyncSession, ingress_http: IngressHTTP) -> None:
    """Edit an existing HTTP ingress configuration.

    Args:
        session: The database session.
        ingress_http: The IngressHTTP object to edit.

    """
    await IngressHTTPPersistor(session, http_ingress_search).edit(ingress_http)


@async_daosession
async def delete(session: AsyncSession, ingress_http: IngressHTTP) -> None:
    """Delete an HTTP ingress configuration.

    Args:
        session: The database session.
        ingress_http: The IngressHTTP object to delete.

    """
    await IngressHTTPPersistor(session, http_ingress_search).delete(ingress_http)
