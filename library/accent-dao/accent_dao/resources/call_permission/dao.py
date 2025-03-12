# file: accent_dao/resources/call_permission/dao.py
# Copyright 2025 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import selectinload

from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.call_permission.persistor import CallPermissionPersistor
from accent_dao.resources.call_permission.search import call_permission_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

    from accent_dao.alchemy.rightcall import RightCall as CallPermission
    from accent_dao.resources.utils.search import SearchResult
    from sqlalchemy.orm import Load
    from sqlalchemy.orm.strategy_options import loader_option

preload_relationships = (
    selectinload(CallPermission.rightcall_groups)
    .selectinload("group")
    .load_only("uuid", "id", "name"),
    selectinload(CallPermission.rightcall_users)
    .selectinload("user")
    .load_only("uuid", "firstname", "webi_lastname"),
    selectinload(CallPermission.rightcall_outcalls)
    .selectinload("outcall")
    .load_only("id", "name"),
    selectinload(CallPermission.rightcallextens),
)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for call permissions.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.
    """
    return await CallPermissionPersistor(
        session, call_permission_search, tenant_uuids
    ).search(parameters)


@async_daosession
async def get(
    session: AsyncSession,
    call_permission_id: int,
    tenant_uuids: list[str] | None = None,
) -> CallPermission:
    """Get a call permission by ID.

    Args:
        session: The database session.
        call_permission_id: The ID of the call permission.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        CallPermission: The call permission.
    """
    return await CallPermissionPersistor(
        session, call_permission_search, tenant_uuids
    ).get_by({"id": call_permission_id})


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> CallPermission:
    """Get a call permission by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        CallPermission: The call permission.
    """
    return await CallPermissionPersistor(
        session, call_permission_search, tenant_uuids
    ).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession,
    call_permission_id: int,
    tenant_uuids: list[str] | None = None,
) -> CallPermission | None:
    """Find a call permission by ID.

    Args:
        session: The database session.
        call_permission_id: The ID of the call permission.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        CallPermission | None: The call permission, or None if not found.
    """
    return await CallPermissionPersistor(
        session, call_permission_search, tenant_uuids
    ).find_by({"id": call_permission_id})


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> CallPermission | None:
    """Find a call permission by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        CallPermission | None: The call permission, or None if not found.
    """
    return await CallPermissionPersistor(
        session, call_permission_search, tenant_uuids
    ).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[CallPermission]:
    """Find all call permissions by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        list[CallPermission]: A list of call permissions.
    """
    result: Sequence[CallPermission] = await CallPermissionPersistor(
        session, call_permission_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(
    session: AsyncSession, call_permission: CallPermission
) -> CallPermission:
    """Create a new call permission.

    Args:
        session: The database session.
        call_permission: The call permission to create.

    Returns:
        CallPermission: The created call permission.
    """
    return await CallPermissionPersistor(session, call_permission_search).create(
        call_permission
    )


@async_daosession
async def edit(session: AsyncSession, call_permission: CallPermission) -> None:
    """Edit an existing call permission.

    Args:
        session: The database session.
        call_permission: The call permission to edit.
    """
    await CallPermissionPersistor(session, call_permission_search).edit(call_permission)


@async_daosession
async def delete(session: AsyncSession, call_permission: CallPermission) -> None:
    """Delete a call permission.

    Args:
        session: The database session.
        call_permission: The call permission to delete.
    """
    await CallPermissionPersistor(session, call_permission_search).delete(
        call_permission
    )


@async_daosession
async def associate_call_permission(
    session: AsyncSession, group: Any, call_permission: Any
) -> None:
    """Associate a call permission.
    This is place holder.

    Args:
        session: The database session.
        group: The group.
        call_permission: The call permission.
    """
    # This is a place holder for the associate_call_permission
    pass


@async_daosession
async def dissociate_call_permission(
    session: AsyncSession, group: Any, call_permission: Any
) -> None:
    """Dissociate a call permission.
    This is place holder.

    Args:
        session: The database session.
        group: The group.
        call_permission: The call permission.
    """
    # This is place holder for the dissociate_call_permission
    pass


@contextmanager
def query_options(*options: Load | loader_option):
    """Query options context"""
    with CallPermissionPersistor.context_query_options(*options):
        yield
