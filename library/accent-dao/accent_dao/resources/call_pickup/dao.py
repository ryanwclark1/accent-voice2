# /resources/call_pickup/dao.py
# Copyright 2025 Accent Communications

import logging
from functools import lru_cache
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from accent_dao.helpers.db_manager import async_daosession, daosession

from .persistor import CallPickupPersistor
from .search import call_pickup_search

logger = logging.getLogger(__name__)


@daosession
def _persistor(
    session: Session, tenant_uuids: list[str] | None = None
) -> CallPickupPersistor:
    """Create a CallPickupPersistor instance.

    Args:
        session: SQLAlchemy session
        tenant_uuids: Optional list of tenant UUIDs

    Returns:
        CallPickupPersistor instance

    """
    return CallPickupPersistor(session, call_pickup_search, tenant_uuids)


@lru_cache(maxsize=128)
async def _async_persistor(
    session: AsyncSession, tenant_uuids: list[str] | None = None
) -> CallPickupPersistor:
    """Create a CallPickupPersistor instance for async operations.

    Args:
        session: SQLAlchemy async session
        tenant_uuids: Optional list of tenant UUIDs

    Returns:
        CallPickupPersistor instance

    """
    return CallPickupPersistor(session, call_pickup_search, tenant_uuids)


@daosession
def search(
    session: Session, tenant_uuids: list[str] | None = None, **parameters: Any
) -> list[Any]:
    """Search for call pickups based on parameters.

    Args:
        session: SQLAlchemy session
        tenant_uuids: Optional list of tenant UUIDs
        parameters: Search parameters

    Returns:
        List of matching call pickup objects

    """
    return _persistor(session, tenant_uuids).search(parameters)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: Any
) -> list[Any]:
    """Search for call pickups based on parameters asynchronously.

    Args:
        session: SQLAlchemy async session
        tenant_uuids: Optional list of tenant UUIDs
        parameters: Search parameters

    Returns:
        List of matching call pickup objects

    """
    persistor = await _async_persistor(session, tenant_uuids)
    return await persistor.async_search(parameters)


@daosession
def get(
    session: Session, call_pickup_id: int, tenant_uuids: list[str] | None = None
) -> Any:
    """Get a call pickup by ID.

    Args:
        session: SQLAlchemy session
        call_pickup_id: Call pickup ID
        tenant_uuids: Optional list of tenant UUIDs

    Returns:
        Call pickup object

    Raises:
        NotFoundError: If call pickup is not found

    """
    return _persistor(session, tenant_uuids).get_by({"id": call_pickup_id})


@async_daosession
async def async_get(
    session: AsyncSession, call_pickup_id: int, tenant_uuids: list[str] | None = None
) -> Any:
    """Get a call pickup by ID asynchronously.

    Args:
        session: SQLAlchemy async session
        call_pickup_id: Call pickup ID
        tenant_uuids: Optional list of tenant UUIDs

    Returns:
        Call pickup object

    Raises:
        NotFoundError: If call pickup is not found

    """
    persistor = await _async_persistor(session, tenant_uuids)
    return await persistor.async_get_by({"id": call_pickup_id})


@daosession
def get_by(
    session: Session, tenant_uuids: list[str] | None = None, **criteria: Any
) -> Any:
    """Get a call pickup by criteria.

    Args:
        session: SQLAlchemy session
        tenant_uuids: Optional list of tenant UUIDs
        criteria: Search criteria

    Returns:
        Call pickup object

    Raises:
        NotFoundError: If call pickup is not found

    """
    return _persistor(session, tenant_uuids).get_by(criteria)


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: Any
) -> Any:
    """Get a call pickup by criteria asynchronously.

    Args:
        session: SQLAlchemy async session
        tenant_uuids: Optional list of tenant UUIDs
        criteria: Search criteria

    Returns:
        Call pickup object

    Raises:
        NotFoundError: If call pickup is not found

    """
    persistor = await _async_persistor(session, tenant_uuids)
    return await persistor.async_get_by(criteria)


@daosession
def find(
    session: Session, call_pickup_id: int, tenant_uuids: list[str] | None = None
) -> Any | None:
    """Find a call pickup by ID.

    Args:
        session: SQLAlchemy session
        call_pickup_id: Call pickup ID
        tenant_uuids: Optional list of tenant UUIDs

    Returns:
        Call pickup object or None if not found

    """
    return _persistor(session, tenant_uuids).find_by({"id": call_pickup_id})


@async_daosession
async def async_find(
    session: AsyncSession, call_pickup_id: int, tenant_uuids: list[str] | None = None
) -> Any | None:
    """Find a call pickup by ID asynchronously.

    Args:
        session: SQLAlchemy async session
        call_pickup_id: Call pickup ID
        tenant_uuids: Optional list of tenant UUIDs

    Returns:
        Call pickup object or None if not found

    """
    persistor = await _async_persistor(session, tenant_uuids)
    return await persistor.async_find_by({"id": call_pickup_id})


@daosession
def find_by(
    session: Session, tenant_uuids: list[str] | None = None, **criteria: Any
) -> Any | None:
    """Find a call pickup by criteria.

    Args:
        session: SQLAlchemy session
        tenant_uuids: Optional list of tenant UUIDs
        criteria: Search criteria

    Returns:
        Call pickup object or None if not found

    """
    return _persistor(session, tenant_uuids).find_by(criteria)


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: Any
) -> Any | None:
    """Find a call pickup by criteria asynchronously.

    Args:
        session: SQLAlchemy async session
        tenant_uuids: Optional list of tenant UUIDs
        criteria: Search criteria

    Returns:
        Call pickup object or None if not found

    """
    persistor = await _async_persistor(session, tenant_uuids)
    return await persistor.async_find_by(criteria)


@daosession
def find_all_by(
    session: Session, tenant_uuids: list[str] | None = None, **criteria: Any
) -> list[Any]:
    """Find all call pickups matching criteria.

    Args:
        session: SQLAlchemy session
        tenant_uuids: Optional list of tenant UUIDs
        criteria: Search criteria

    Returns:
        List of matching call pickup objects

    """
    return _persistor(session, tenant_uuids).find_all_by(criteria)


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: Any
) -> list[Any]:
    """Find all call pickups matching criteria asynchronously.

    Args:
        session: SQLAlchemy async session
        tenant_uuids: Optional list of tenant UUIDs
        criteria: Search criteria

    Returns:
        List of matching call pickup objects

    """
    persistor = await _async_persistor(session, tenant_uuids)
    return await persistor.async_find_all_by(criteria)


@daosession
def create(session: Session, call_pickup: Any) -> Any:
    """Create a new call pickup.

    Args:
        session: SQLAlchemy session
        call_pickup: Call pickup object to create

    Returns:
        Created call pickup object

    """
    logger.info("Creating new call pickup")
    return _persistor(session).create(call_pickup)


@async_daosession
async def async_create(session: AsyncSession, call_pickup: Any) -> Any:
    """Create a new call pickup asynchronously.

    Args:
        session: SQLAlchemy async session
        call_pickup: Call pickup object to create

    Returns:
        Created call pickup object

    """
    logger.info("Creating new call pickup asynchronously")
    persistor = await _async_persistor(session)
    return await persistor.async_create(call_pickup)


@daosession
def edit(session: Session, call_pickup: Any) -> None:
    """Edit an existing call pickup.

    Args:
        session: SQLAlchemy session
        call_pickup: Call pickup object to edit

    """
    logger.info("Editing call pickup with ID %s", call_pickup.id)
    _persistor(session).edit(call_pickup)


@async_daosession
async def async_edit(session: AsyncSession, call_pickup: Any) -> None:
    """Edit an existing call pickup asynchronously.

    Args:
        session: SQLAlchemy async session
        call_pickup: Call pickup object to edit

    """
    logger.info("Editing call pickup with ID %s asynchronously", call_pickup.id)
    persistor = await _async_persistor(session)
    await persistor.async_edit(call_pickup)


@daosession
def delete(session: Session, call_pickup: Any) -> None:
    """Delete a call pickup.

    Args:
        session: SQLAlchemy session
        call_pickup: Call pickup object to delete

    """
    logger.info("Deleting call pickup with ID %s", call_pickup.id)
    _persistor(session).delete(call_pickup)


@async_daosession
async def async_delete(session: AsyncSession, call_pickup: Any) -> None:
    """Delete a call pickup asynchronously.

    Args:
        session: SQLAlchemy async session
        call_pickup: Call pickup object to delete

    """
    logger.info("Deleting call pickup with ID %s asynchronously", call_pickup.id)
    persistor = await _async_persistor(session)
    await persistor.async_delete(call_pickup)


@daosession
def associate_interceptor_users(
    session: Session, call_pickup: Any, users: list[Any]
) -> None:
    """Associate interceptor users with a call pickup.

    Args:
        session: SQLAlchemy session
        call_pickup: Call pickup object
        users: List of user objects to associate

    """
    logger.info(
        "Associating %s interceptor users with call pickup ID %s",
        len(users),
        call_pickup.id,
    )
    _persistor(session).associate_interceptor_users(call_pickup, users)


@async_daosession
async def async_associate_interceptor_users(
    session: AsyncSession, call_pickup: Any, users: list[Any]
) -> None:
    """Associate interceptor users with a call pickup asynchronously.

    Args:
        session: SQLAlchemy async session
        call_pickup: Call pickup object
        users: List of user objects to associate

    """
    logger.info(
        "Associating %s interceptor users with call pickup ID %s asynchronously",
        len(users),
        call_pickup.id,
    )
    persistor = await _async_persistor(session)
    await persistor.async_associate_interceptor_users(call_pickup, users)


@daosession
def associate_interceptor_groups(
    session: Session, call_pickup: Any, groups: list[Any]
) -> None:
    """Associate interceptor groups with a call pickup.

    Args:
        session: SQLAlchemy session
        call_pickup: Call pickup object
        groups: List of group objects to associate

    """
    logger.info(
        "Associating %s interceptor groups with call pickup ID %s",
        len(groups),
        call_pickup.id,
    )
    _persistor(session).associate_interceptor_groups(call_pickup, groups)


@async_daosession
async def async_associate_interceptor_groups(
    session: AsyncSession, call_pickup: Any, groups: list[Any]
) -> None:
    """Associate interceptor groups with a call pickup asynchronously.

    Args:
        session: SQLAlchemy async session
        call_pickup: Call pickup object
        groups: List of group objects to associate

    """
    logger.info(
        "Associating %s interceptor groups with call pickup ID %s asynchronously",
        len(groups),
        call_pickup.id,
    )
    persistor = await _async_persistor(session)
    await persistor.async_associate_interceptor_groups(call_pickup, groups)


@daosession
def associate_target_users(
    session: Session, call_pickup: Any, users: list[Any]
) -> None:
    """Associate target users with a call pickup.

    Args:
        session: SQLAlchemy session
        call_pickup: Call pickup object
        users: List of user objects to associate

    """
    logger.info(
        "Associating %s target users with call pickup ID %s", len(users), call_pickup.id
    )
    _persistor(session).associate_target_users(call_pickup, users)


@async_daosession
async def async_associate_target_users(
    session: AsyncSession, call_pickup: Any, users: list[Any]
) -> None:
    """Associate target users with a call pickup asynchronously.

    Args:
        session: SQLAlchemy async session
        call_pickup: Call pickup object
        users: List of user objects to associate

    """
    logger.info(
        "Associating %s target users with call pickup ID %s asynchronously",
        len(users),
        call_pickup.id,
    )
    persistor = await _async_persistor(session)
    await persistor.async_associate_target_users(call_pickup, users)


@daosession
def associate_target_groups(
    session: Session, call_pickup: Any, groups: list[Any]
) -> None:
    """Associate target groups with a call pickup.

    Args:
        session: SQLAlchemy session
        call_pickup: Call pickup object
        groups: List of group objects to associate

    """
    logger.info(
        "Associating %s target groups with call pickup ID %s",
        len(groups),
        call_pickup.id,
    )
    _persistor(session).associate_target_groups(call_pickup, groups)


@async_daosession
async def async_associate_target_groups(
    session: AsyncSession, call_pickup: Any, groups: list[Any]
) -> None:
    """Associate target groups with a call pickup asynchronously.

    Args:
        session: SQLAlchemy async session
        call_pickup: Call pickup object
        groups: List of group objects to associate

    """
    logger.info(
        "Associating %s target groups with call pickup ID %s asynchronously",
        len(groups),
        call_pickup.id,
    )
    persistor = await _async_persistor(session)
    await persistor.async_associate_target_groups(call_pickup, groups)
