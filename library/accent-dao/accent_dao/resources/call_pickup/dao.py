# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.pickup import Pickup as CallPickup
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.call_pickup.persistor import CallPickupPersistor
from accent_dao.resources.call_pickup.search import call_pickup_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.alchemy.groupfeatures import GroupFeatures
    from accent_dao.alchemy.userfeatures import UserFeatures
    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for call pickups.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of call pickups.

    """
    return await CallPickupPersistor(session, call_pickup_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def get(
    session: AsyncSession, call_pickup_id: int, tenant_uuids: list[str] | None = None
) -> CallPickup:
    """Get a call pickup by ID.

    Args:
        session: The database session.
        call_pickup_id: The ID of the call pickup.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The call pickup object.

    """
    return await CallPickupPersistor(session, call_pickup_search, tenant_uuids).get_by(
        {"id": call_pickup_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> CallPickup:
    """Get a call pickup by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The call pickup object.

    """
    return await CallPickupPersistor(session, call_pickup_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def find(
    session: AsyncSession, call_pickup_id: int, tenant_uuids: list[str] | None = None
) -> CallPickup | None:
    """Find a call pickup by ID.

    Args:
        session: The database session.
        call_pickup_id: The ID of the call pickup.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The call pickup object or None if not found.

    """
    return await CallPickupPersistor(session, call_pickup_search, tenant_uuids).find_by(
        {"id": call_pickup_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> CallPickup | None:
    """Find a call pickup by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The call pickup object or None if not found.

    """
    return await CallPickupPersistor(session, call_pickup_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[CallPickup]:
    """Find all call pickups by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of call pickup objects.

    """
    result: Sequence[CallPickup] = await CallPickupPersistor(
        session, call_pickup_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, call_pickup: CallPickup) -> CallPickup:
    """Create a new call pickup.

    Args:
        session: The database session.
        call_pickup: The call pickup object to create.

    Returns:
        The created call pickup object.

    """
    return await CallPickupPersistor(session, call_pickup_search).create(call_pickup)


@async_daosession
async def edit(session: AsyncSession, call_pickup: CallPickup) -> None:
    """Edit an existing call pickup.

    Args:
        session: The database session.
        call_pickup: The call pickup object to edit.

    """
    await CallPickupPersistor(session, call_pickup_search).edit(call_pickup)


@async_daosession
async def delete(session: AsyncSession, call_pickup: CallPickup) -> None:
    """Delete a call pickup.

    Args:
        session: The database session.
        call_pickup: The call pickup object to delete.

    """
    await CallPickupPersistor(session, call_pickup_search).delete(call_pickup)


@async_daosession
async def associate_interceptor_users(
    session: AsyncSession, call_pickup: CallPickup, users: list["UserFeatures"]
) -> None:
    """Associate interceptor users with a call pickup.

    Args:
        session: The database session.
        call_pickup: The call pickup object.
        users: A list of UserFeatures objects to associate.

    """
    await CallPickupPersistor(session, call_pickup_search).associate_interceptor_users(
        call_pickup, users
    )


@async_daosession
async def associate_interceptor_groups(
    session: AsyncSession, call_pickup: CallPickup, groups: list["GroupFeatures"]
) -> None:
    """Associate interceptor groups with a call pickup.

    Args:
        session: The database session.
        call_pickup: The call pickup object.
        groups: A list of GroupFeatures objects to associate.

    """
    await CallPickupPersistor(session, call_pickup_search).associate_interceptor_groups(
        call_pickup, groups
    )


@async_daosession
async def associate_target_users(
    session: AsyncSession, call_pickup: CallPickup, users: list["UserFeatures"]
) -> None:
    """Associate target users with a call pickup.

    Args:
        session: The database session.
        call_pickup: The call pickup object.
        users: A list of UserFeatures objects to associate.

    """
    await CallPickupPersistor(session, call_pickup_search).associate_target_users(
        call_pickup, users
    )


@async_daosession
async def associate_target_groups(
    session: AsyncSession, call_pickup: CallPickup, groups: list["GroupFeatures"]
) -> None:
    """Associate target groups with a call pickup.

    Args:
        session: The database session.
        call_pickup: The call pickup object.
        groups: A list of GroupFeatures objects to associate.

    """
    await CallPickupPersistor(session, call_pickup_search).associate_target_groups(
        call_pickup, groups
    )
