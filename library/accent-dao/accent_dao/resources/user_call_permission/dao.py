# file: accent_dao/resources/user_call_permission/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.rightcallmember import RightCallMember as UserCallPermission
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.helpers.exception import InputError
from accent_dao.resources.user_call_permission.persistor import UserCallPermissionPersistor

# Configure logging
logger = logging.getLogger(__name__)


@async_daosession
async def get_by(session: AsyncSession, **criteria: dict) -> UserCallPermission:
    """Get a user call permission by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The user call permission.

    Raises:
        NotFoundError: If no user call permission is found with the given criteria.

    """
    return await UserCallPermissionPersistor(session).get_by(criteria)


@async_daosession
async def find_by(
    session: AsyncSession, **criteria: dict
) -> UserCallPermission | None:
    """Find a user call permission by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The user call permission or None if not found.

    """
    return await UserCallPermissionPersistor(session).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, **criteria: dict
) -> list[UserCallPermission]:
    """Find all user call permissions by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of user call permissions.

    """
    return await UserCallPermissionPersistor(session).find_all_by(criteria)


@async_daosession
async def associate(
    session: AsyncSession, user: Any, call_permission: Any
) -> UserCallPermission:
    """Associate a user with a call permission.

    Args:
        session: The database session.
        user: The user object.
        call_permission: The call permission object.

    Returns:
        The created or existing UserCallPermission object.

    """
    return await UserCallPermissionPersistor(session).associate_user_call_permission(
        user, call_permission
    )


@async_daosession
async def dissociate(
    session: AsyncSession, user: Any, call_permission: Any
) -> None:
    """Dissociate a user from a call permission.

    Args:
        session: The database session.
        user: The user object.
        call_permission: The call permission object.

    """
    await UserCallPermissionPersistor(session).dissociate_user_call_permission(
        user, call_permission
    )


@async_daosession
async def dissociate_all_by_user(session: AsyncSession, user: Any) -> None:
    """Dissociate all call permissions from a user.

    Args:
        session: The database session.
        user: The user object.

    """
    await UserCallPermissionPersistor(session).dissociate_all_call_permissions_by_user(
        user
    )
