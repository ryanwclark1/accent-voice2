# Copyright 2025 Accent Communications

import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.groupfeatures import GroupFeatures
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import GroupPersistor
from .search import group_search

if TYPE_CHECKING:
    from accent_dao.alchemy.rightcall import RightCall
    from accent_dao.alchemy.queuemember import QueueMember

logger: logging.Logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for groups.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of groups.

    """
    return await GroupPersistor(session, group_search, tenant_uuids).search(parameters)


@async_daosession
async def get(
    session: AsyncSession, group_id: int | str, tenant_uuids: list[str] | None = None
) -> GroupFeatures:
    """Get a group by ID or UUID.

    Args:
        session: The database session.
        group_id: The ID or UUID of the group.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The group object.

    """
    field, value = _id_to_field_value(group_id)
    return await GroupPersistor(session, group_search, tenant_uuids).get_by(
        {field: value}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> GroupFeatures:
    """Get a group by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The group object.

    """
    return await GroupPersistor(session, group_search, tenant_uuids).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession, group_id: int | str, tenant_uuids: list[str] | None = None
) -> GroupFeatures | None:
    """Find a group by ID or UUID.

    Args:
        session: The database session.
        group_id: The ID or UUID of the group.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The group object or None if not found.

    """
    field, value = _id_to_field_value(group_id)
    return await GroupPersistor(session, group_search, tenant_uuids).find_by(
        {field: value}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> GroupFeatures | None:
    """Find a group by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The group object or None if not found.

    """
    return await GroupPersistor(session, group_search, tenant_uuids).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[GroupFeatures]:
    """Find all groups by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of group objects.

    """
    return await GroupPersistor(session, group_search, tenant_uuids).find_all_by(
        criteria
    )


@async_daosession
async def create(session: AsyncSession, group: GroupFeatures) -> GroupFeatures:
    """Create a new group.

    Args:
        session: The database session.
        group: The group object to create.

    Returns:
        The created group object.

    """
    return await GroupPersistor(session, group_search).create(group)


@async_daosession
async def edit(session: AsyncSession, group: GroupFeatures) -> None:
    """Edit an existing group.

    Args:
        session: The database session.
        group: The group object to edit.

    """
    await GroupPersistor(session, group_search).edit(group)


@async_daosession
async def delete(session: AsyncSession, group: GroupFeatures) -> None:
    """Delete a group.

    Args:
        session: The database session.
        group: The group object to delete.

    """
    await GroupPersistor(session, group_search).delete(group)


@async_daosession
async def associate_all_member_users(
    session: AsyncSession, group: GroupFeatures, members: Sequence[QueueMember]
) -> None:
    """Associate all user members with a group.

    Args:
        session: The database session.
        group: The group object.
        members: A sequence of QueueMember objects representing users.

    """
    await GroupPersistor(session, group_search).associate_all_member_users(
        group, members
    )


@async_daosession
async def associate_all_member_extensions(
    session: AsyncSession, group: GroupFeatures, members: Sequence[QueueMember]
) -> None:
    """Associate all extension members with a group.

    Args:
        session: The database session.
        group: The group object.
        members: A sequence of QueueMember objects representing extensions.

    """
    await GroupPersistor(session, group_search).associate_all_member_extensions(
        group, members
    )


@async_daosession
async def associate_call_permission(
    session: AsyncSession, group: GroupFeatures, call_permission: "RightCall"
) -> None:
    """Associate a call permission with a group.

    Args:
        session: The database session.
        group: The group object.
        call_permission: The call permission object to associate.

    """
    await GroupPersistor(session, group_search).associate_call_permission(
        group, call_permission
    )


@async_daosession
async def dissociate_call_permission(
    session: AsyncSession, group: GroupFeatures, call_permission: "RightCall"
) -> None:
    """Dissociate a call permission from a group.

    Args:
        session: The database session.
        group: The group object.
        call_permission: The call permission object to dissociate.

    """
    await GroupPersistor(session, group_search).dissociate_call_permission(
        group, call_permission
    )


def _id_to_field_value(id_or_uuid: int | str) -> tuple[str, int | str]:
    """Convert ID or UUID to field and value.

    Args:
        id_or_uuid: The ID or UUID.

    Returns:
        A tuple containing the field name and value.

    Raises:
        ValueError: If the input is not a valid integer or UUID string.

    """
    try:
        return "id", int(id_or_uuid)
    except (ValueError, TypeError):
        try:
            uuid_obj = UUID(str(id_or_uuid), version=4)
            return "uuid", str(uuid_obj)
        except (ValueError, TypeError) as e:
            logger.error("Invalid input for ID or UUID: %s", id_or_uuid)
            raise ValueError(f"Invalid input for ID or UUID: {id_or_uuid}") from e
