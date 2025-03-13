# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from accent_dao.alchemy.rightcallmember import RightCallMember
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.user.persistor import UserPersistor
from accent_dao.resources.user.search import user_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.alchemy.groupfeatures import GroupFeatures
    from accent_dao.alchemy.rightcall import RightCall
    from accent_dao.resources.utils.search import SearchResult

from .fixes import UserFixes
from .persistor import UserPersistor
from .search import user_search
from .view import user_view

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for users.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of users.

    """
    return await UserPersistor(session, user_view, user_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def search_collated(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for users, with additional collation.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of users.

    """
    return await UserPersistor(
        session, user_view, user_search, tenant_uuids
    ).search_collated(parameters)


@async_daosession
async def get(
    session: AsyncSession, user_id: int, tenant_uuids: list[str] | None = None
) -> UserFeatures:
    """Get a user by ID.

    Args:
        session: The database session.
        user_id: The ID of the user.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The user object.

    """
    return await UserPersistor(session, user_view, user_search, tenant_uuids).get_by(
        {"id": user_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> UserFeatures:
    """Get a user by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The user object.

    """
    return await UserPersistor(session, user_view, user_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def find(
    session: AsyncSession, user_id: int, tenant_uuids: list[str] | None = None
) -> UserFeatures | None:
    """Find a user by ID.

    Args:
        session: The database session.
        user_id: The ID of the user.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The user object or None if not found.

    """
    return await UserPersistor(session, user_view, user_search, tenant_uuids).find_by(
        {"id": user_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> UserFeatures | None:
    """Find a user by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The user object or None if not found.

    """
    return await UserPersistor(session, user_view, user_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[UserFeatures]:
    """Find all users by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of user objects.

    """
    result: Sequence[UserFeatures] = await UserPersistor(
        session, user_view, user_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def get_by_id_uuid(
    session: AsyncSession, id: int | str, tenant_uuids: list[str] | None = None
) -> UserFeatures:
    """Get a user by ID or UUID.

    Args:
        session: The database session.
        id: The ID or UUID of the user.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The user object.

    """
    return await UserPersistor(
        session, user_view, user_search, tenant_uuids
    ).get_by_id_uuid(id)


@async_daosession
async def find_by_id_uuid(
    session: AsyncSession, id: int | str, tenant_uuids: list[str] | None = None
) -> UserFeatures | None:
    """Find a user by ID or UUID.

    Args:
        session: The database session.
        id: The ID or UUID of the user.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The user object or None if not found.

    """
    return await UserPersistor(
        session, user_view, user_search, tenant_uuids
    ).find_by_id_uuid(id)


@async_daosession
async def find_all_by_agent_id(
    session: AsyncSession, agent_id: int, tenant_uuids: list[str] | None = None
) -> list[UserFeatures]:
    """Find all users associated with an agent ID.

    Args:
        session: The database session.
        agent_id: The ID of the agent.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        A list of user objects.

    """
    result: Sequence[UserFeatures] = await UserPersistor(
        session, user_view, user_search, tenant_uuids
    ).find_all_by({"agentid": agent_id})
    return list(result)


@async_daosession
async def create(session: AsyncSession, user: UserFeatures) -> UserFeatures:
    """Create a new user.

    Args:
        session: The database session.
        user: The user object to create.

    Returns:
        The created user object.

    """
    return await UserPersistor(session, user_view, user_search).create(user)


@async_daosession
async def edit(session: AsyncSession, user: UserFeatures) -> None:
    """Edit an existing user.

    Args:
        session: The database session.
        user: The user object to edit.

    """
    await UserPersistor(session, user_view, user_search).edit(user)

    await UserFixes(session).fix(user.id)


@async_daosession
async def delete(session: AsyncSession, user: UserFeatures) -> None:
    """Delete a user.

    Args:
        session: The database session.
        user: The user object to delete.

    """
    await UserPersistor(session, user_view, user_search).delete(user)


@async_daosession
async def associate_all_groups(
    session: AsyncSession, user: UserFeatures, groups: list["GroupFeatures"]
) -> None:
    """Associate all groups with a user.

    Args:
        session: The database session.
        user: The user object.
        groups: The list of group objects.

    """
    await UserPersistor(session, user_view, user_search).associate_all_groups(user, groups)


@async_daosession
async def dissociate_call_permission(
    session: AsyncSession, user: UserFeatures, call_permission: "RightCall"
) -> None:
    """Dissociate a call permission from a user.

    Args:
        session: The database session.
        user: The user object.
        call_permission: The call permission object to dissociate.

    """
    await UserPersistor(session, user_view, user_search).dissociate_call_permission(
        user, call_permission
    )


@async_daosession
async def list_outgoing_callerid_associated(
    session: AsyncSession, user_id: int
) -> list[dict[str, str]]:
    """List outgoing caller ID associations for a user.

    Args:
        session: The database session.
        user_id: The ID of the user.

    Returns:
        A list of dictionaries with 'number' and 'type' keys.

    """
    return await UserPersistor(session, user_view, user_search).list_outgoing_callerid_associated(
        user_id
    )
