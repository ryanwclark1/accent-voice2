# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.user_external_app import UserExternalApp
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.user_external_app.persistor import (
    UserExternalAppPersistor,
)
from accent_dao.resources.user_external_app.search import user_external_app_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, user_uuid: str, **parameters: dict
) -> "SearchResult":
    """Search for user external apps.

    Args:
        session: The database session.
        user_uuid: The UUID of the user.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of user external apps.

    """
    return await UserExternalAppPersistor(
        session, user_external_app_search, user_uuid
    ).search(parameters)


@async_daosession
async def get(
    session: AsyncSession, user_uuid: str, external_app_name: str
) -> UserExternalApp:
    """Get a user external app by name.

    Args:
        session: The database session.
        user_uuid: The UUID of the user.
        external_app_name: The name of the external app.

    Returns:
        The UserExternalApp object.

    """
    return await UserExternalAppPersistor(
        session, user_external_app_search, user_uuid
    ).get_by({"name": external_app_name})


@async_daosession
async def get_by(
    session: AsyncSession, user_uuid: str, **criteria: dict
) -> UserExternalApp:
    """Get a user external app by criteria.

    Args:
        session: The database session.
        user_uuid: The UUID of the user.
        **criteria: Keyword arguments for filtering.

    Returns:
        The UserExternalApp object.

    """
    return await UserExternalAppPersistor(
        session, user_external_app_search, user_uuid
    ).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession, user_uuid: str, external_app_name: str
) -> UserExternalApp | None:
    """Find a user external app by name.

    Args:
        session: The database session.
        user_uuid: The UUID of the user.
        external_app_name: The name of the external app.

    Returns:
        The UserExternalApp object or None if not found.

    """
    return await UserExternalAppPersistor(
        session, user_external_app_search, user_uuid
    ).find_by({"name": external_app_name})


@async_daosession
async def find_by(
    session: AsyncSession, user_uuid: str, **criteria: dict
) -> UserExternalApp | None:
    """Find a user external app by criteria.

    Args:
        session: The database session.
        user_uuid: The UUID of the user.
        **criteria: Keyword arguments for filtering.

    Returns:
        The UserExternalApp object or None if not found.

    """
    return await UserExternalAppPersistor(
        session, user_external_app_search, user_uuid
    ).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, user_uuid: str, **criteria: dict
) -> list[UserExternalApp]:
    """Find all user external apps by criteria.

    Args:
        session: The database session.
        user_uuid: The UUID of the user.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of UserExternalApp objects.

    """
    result: Sequence[UserExternalApp] = await UserExternalAppPersistor(
        session, user_external_app_search, user_uuid
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(
    session: AsyncSession, external_app: UserExternalApp
) -> UserExternalApp:
    """Create a new user external app.

    Args:
        session: The database session.
        external_app: The UserExternalApp object to create.

    Returns:
        The created UserExternalApp object.

    """
    return await UserExternalAppPersistor(session, user_external_app_search).create(
        external_app
    )


@async_daosession
async def edit(session: AsyncSession, external_app: UserExternalApp) -> None:
    """Edit an existing user external app.

    Args:
        session: The database session.
        external_app: The UserExternalApp object to edit.

    """
    await UserExternalAppPersistor(session, user_external_app_search).edit(external_app)


@async_daosession
async def delete(session: AsyncSession, external_app: UserExternalApp) -> None:
    """Delete a user external app.

    Args:
        session: The database session.
        external_app: The UserExternalApp object to delete.

    """
    await UserExternalAppPersistor(session, user_external_app_search).delete(
        external_app
    )
