# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.parking_lot import ParkingLot
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.parking_lot.persistor import ParkingLotPersistor
from accent_dao.resources.parking_lot.search import parking_lot_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for parking lots.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of parking lots.

    """
    return await ParkingLotPersistor(session, parking_lot_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def get(
    session: AsyncSession, parking_lot_id: int, tenant_uuids: list[str] | None = None
) -> ParkingLot:
    """Get a parking lot by ID.

    Args:
        session: The database session.
        parking_lot_id: The ID of the parking lot.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The parking lot object.

    """
    return await ParkingLotPersistor(session, parking_lot_search, tenant_uuids).get_by(
        {"id": parking_lot_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> ParkingLot:
    """Get a parking lot by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The parking lot object.

    """
    return await ParkingLotPersistor(session, parking_lot_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def find(
    session: AsyncSession, parking_lot_id: int, tenant_uuids: list[str] | None = None
) -> ParkingLot | None:
    """Find a parking lot by ID.

    Args:
        session: The database session.
        parking_lot_id: The ID of the parking lot.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The parking lot object or None if not found.

    """
    return await ParkingLotPersistor(session, parking_lot_search, tenant_uuids).find_by(
        {"id": parking_lot_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> ParkingLot | None:
    """Find a parking lot by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The parking lot object or None if not found.

    """
    return await ParkingLotPersistor(session, parking_lot_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[ParkingLot]:
    """Find all parking lots by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of parking lot objects.

    """
    result: Sequence[ParkingLot] = await ParkingLotPersistor(
        session, parking_lot_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, parking_lot: ParkingLot) -> ParkingLot:
    """Create a new parking lot.

    Args:
        session: The database session.
        parking_lot: The parking lot object to create.

    Returns:
        The created parking lot object.

    """
    return await ParkingLotPersistor(session, parking_lot_search).create(parking_lot)


@async_daosession
async def edit(session: AsyncSession, parking_lot: ParkingLot) -> None:
    """Edit an existing parking lot.

    Args:
        session: The database session.
        parking_lot: The parking lot object to edit.

    """
    await ParkingLotPersistor(session, parking_lot_search).edit(parking_lot)


@async_daosession
async def delete(session: AsyncSession, parking_lot: ParkingLot) -> None:
    """Delete a parking lot.

    Args:
        session: The database session.
        parking_lot: The parking lot object to delete.

    """
    await ParkingLotPersistor(session, parking_lot_search).delete(parking_lot)
