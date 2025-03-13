# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.incall import Incall
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.incall.persistor import IncallPersistor
from accent_dao.resources.incall.search import incall_search

if TYPE_CHECKING:
    from accent_dao.alchemy.dialaction import Dialaction
    from accent_dao.resources.utils.search import SearchResult
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for incall routes.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of incalls.

    """
    return await IncallPersistor(session, incall_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def get(
    session: AsyncSession, incall_id: int, tenant_uuids: list[str] | None = None
) -> Incall:
    """Get an incall route by ID.

    Args:
        session: The database session.
        incall_id: The ID of the incall route.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The incall route.

    """
    return await IncallPersistor(session, incall_search, tenant_uuids).get_by(
        {"id": incall_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Incall:
    """Get an incall route by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The incall route.

    """
    return await IncallPersistor(session, incall_search, tenant_uuids).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession, incall_id: int, tenant_uuids: list[str] | None = None
) -> Incall | None:
    """Find an incall route by ID.

    Args:
        session: The database session.
        incall_id: The ID of the incall route.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The incall route or None if not found.

    """
    return await IncallPersistor(session, incall_search, tenant_uuids).find_by(
        {"id": incall_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Incall | None:
    """Find an incall route by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The incall route or None if not found.

    """
    return await IncallPersistor(session, incall_search, tenant_uuids).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Incall]:
    """Find all incall routes by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of incall routes.

    """
    result: Sequence[Incall] = await IncallPersistor(
        session, incall_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, incall: Incall) -> Incall:
    """Create a new incall route.

    Args:
        session: The database session.
        incall: The incall route object to create.

    Returns:
        The created incall route object.

    """
    return await IncallPersistor(session, incall_search).create(incall)


@async_daosession
async def edit(session: AsyncSession, incall: Incall) -> None:
    """Edit an existing incall route.

    Args:
        session: The database session.
        incall: The incall route object to edit.

    """
    await IncallPersistor(session, incall_search).edit(incall)


@async_daosession
async def update_destination(
    session: AsyncSession, incall: Incall, destination: "Dialaction"
) -> None:
    """Update the destination of an incall route.

    Args:
        session: The database session.
        incall: The incall route object.
        destination: The new destination dialaction.

    """
    await IncallPersistor(session, incall_search).update_destination(
        incall, destination
    )


@async_daosession
async def delete(session: AsyncSession, incall: Incall) -> None:
    """Delete an incall route.

    Args:
        session: The database session.
        incall: The incall route object to delete.

    """
    await IncallPersistor(session, incall_search).delete(incall)
