# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.ivr import IVR
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.ivr.persistor import IVRPersistor
from accent_dao.resources.ivr.search import ivr_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.alchemy.dialaction import Dialaction
    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for IVRs.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of IVRs.

    """
    return await IVRPersistor(session, ivr_search, tenant_uuids).search(parameters)


@async_daosession
async def get(
    session: AsyncSession, ivr_id: int, tenant_uuids: list[str] | None = None
) -> IVR:
    """Get an IVR by ID.

    Args:
        session: The database session.
        ivr_id: The ID of the IVR.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The IVR object.

    """
    return await IVRPersistor(session, ivr_search, tenant_uuids).get_by({"id": ivr_id})


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> IVR:
    """Get an IVR by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The IVR object.

    """
    return await IVRPersistor(session, ivr_search, tenant_uuids).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession, ivr_id: int, tenant_uuids: list[str] | None = None
) -> IVR | None:
    """Find an IVR by ID.

    Args:
        session: The database session.
        ivr_id: The ID of the IVR.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The IVR object or None if not found.

    """
    return await IVRPersistor(session, ivr_search, tenant_uuids).find_by({"id": ivr_id})


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> IVR | None:
    """Find an IVR by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The IVR object or None if not found.

    """
    return await IVRPersistor(session, ivr_search, tenant_uuids).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[IVR]:
    """Find all IVRs by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of IVR objects.

    """
    result: Sequence[IVR] = await IVRPersistor(
        session, ivr_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, ivr: IVR) -> IVR:
    """Create a new IVR.

    Args:
        session: The database session.
        ivr: The IVR object to create.

    Returns:
        The created IVR object.

    """
    return await IVRPersistor(session, ivr_search).create(ivr)


@async_daosession
async def edit(session: AsyncSession, ivr: IVR) -> None:
    """Edit an existing IVR.

    Args:
        session: The database session.
        ivr: The IVR object to edit.

    """
    await IVRPersistor(session, ivr_search).edit(ivr)


@async_daosession
async def update_destination(
    session: AsyncSession, ivr: IVR, event: str, destination: "Dialaction"
) -> None:
    """Update a dialaction of the IVR.

    Args:
        session: The database session.
        ivr: The IVR to update.
        event: the event for the dialaction.
        destination: The new Dialaction

    """
    await IVRPersistor(session, ivr_search).update_dialaction(ivr, event, destination)


@async_daosession
async def delete(session: AsyncSession, ivr: IVR) -> None:
    """Delete an IVR.

    Args:
        session: The database session.
        ivr: The IVR object to delete.

    """
    await IVRPersistor(session, ivr_search).delete(ivr)
