# file: accent_dao/resources/user/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.userfeatures import UserFeatures as User
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .fixes import UserFixes
from .persistor import UserPersistor
from .search import user_search
from .view import user_view

logger = logging.getLogger(__name__)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for users.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.

    """
    return await UserPersistor(session, user_view, user_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def async_search_collated(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for users with collation.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.

    """
    return await UserPersistor(
        session, user_view, user_search, tenant_uuids
    ).search_collated(parameters)


@async_daosession
async def async_get(
    session: AsyncSession, user_id: int, tenant_uuids: list[str] | None = None
) -> User:
    """Get a user by ID.

    Args:
        session: The database session.
        user_id: The ID of the user.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The user.

    """
    return await UserPersistor(session, user_view, user_search, tenant_uuids).get_by(
        {"id": user_id}
    )


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> User:
    """Get a user by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The user.

    """
    return await UserPersistor(session, user_view, user_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def async_find_by_id_uuid(
    session: AsyncSession, id: int | str, tenant_uuids: list[str] | None = None
) -> User | None:
    """Find a user by ID or UUID.

    Args:
        session: The database session.
        id: The ID or UUID of the user.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The user if found, None otherwise.

    """
    return await UserPersistor(
        session, user_view, user_search, tenant_uuids
    ).find_by_id_uuid(id)


@async_daosession
async def async_get_by_id_uuid(
    session: AsyncSession, id: int | str, tenant_uuids: list[str] | None = None
) -> User:
    """Get a user by ID or UUID.

    Args:
        session: The database session.
        id: The ID or UUID of the user.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The user.

    """
    return await UserPersistor(
        session, user_view, user_search, tenant_uuids
    ).get_by_id_uuid(id)


@async_daosession
async def async_find_all_by_agent_id(
    session: AsyncSession, agent_id: int
) -> list[User]:
    """Find all users by agent ID.

    Args:
        session: The database session.
        agent_id: The ID of the agent.

    Returns:
        A list of users.

    """
    return await UserPersistor(session, user_view, user_search).find_all_by_agent_id(
        agent_id
    )


@async_daosession
async def async_find(
    session: AsyncSession, user_id: int, tenant_uuids: list[str] | None = None
) -> User | None:
    """Find a user by ID.

    Args:
        session: The database session.
        user_id: The ID of the user.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The user if found, None otherwise.

    """
    return await UserPersistor(session, user_view, user_search, tenant_uuids).find_by(
        {"id": user_id}
    )


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> User | None:
    """Find a user by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The user if found, None otherwise.

    """
    return await UserPersistor(session, user_view, user_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[User]:
    """Find all users by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of users.

    """
    return await UserPersistor(
        session, user_view, user_search, tenant_uuids
    ).find_all_by(criteria)


@async_daosession
async def async_count_all_by(
    session: AsyncSession, column_name: str, **criteria: dict
) -> list:
    """Count all users by criteria.

    Args:
        session: The database session.
        column_name: The column name to group by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of counts.

    """
    return await UserPersistor(session, user_view, user_search).count_all_by(
        column_name, **criteria
    )


@async_daosession
async def async_create(session: AsyncSession, user: User) -> User:
    """Create a new user.

    Args:
        session: The database session.
        user: The user to create.

    Returns:
        The created user.

    """
    return await UserPersistor(session).create(user)


@async_daosession
async def async_edit(session: AsyncSession, user: User) -> None:
    """Edit an existing user.

    Args:
        session: The database session.
        user: The user to edit.

    """
    await UserPersistor(session).edit(user)
    await UserFixes(session).async_fix(user.id)


@async_daosession
async def async_delete(session: AsyncSession, user: User) -> None:
    """Delete a user.

    Args:
        session: The database session.
        user: The user to delete.

    """
    await UserPersistor(session).delete(user)


@async_daosession
async def async_associate_all_groups(
    session: AsyncSession, user: User, groups: list
) -> None:
    """Associate all groups with a user.

    Args:
        session: The database session.
        user: The user.
        groups: The list of groups to associate.

    """
    await UserPersistor(session).associate_all_groups(user, groups)


@async_daosession
async def async_list_outgoing_callerid_associated(
    session: AsyncSession, user_id: int
) -> list:
    """List outgoing caller IDs associated with a user.

    Args:
        session: The database session.
        user_id: The ID of the user.

    Returns:
        A list of associated outgoing caller IDs.

    """
    return await UserPersistor(session).list_outgoing_callerid_associated(user_id)
