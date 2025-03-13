# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.dialpattern import DialPattern
from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.outcall import Outcall
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.outcall.persistor import OutcallPersistor
from accent_dao.resources.outcall.search import outcall_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.alchemy.rightcall import RightCall
    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for outcalls.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of outcalls.

    """
    return await OutcallPersistor(session, outcall_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def get(
    session: AsyncSession, outcall_id: int, tenant_uuids: list[str] | None = None
) -> Outcall:
    """Get an outcall by ID.

    Args:
        session: The database session.
        outcall_id: The ID of the outcall.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The outcall object.

    """
    return await OutcallPersistor(session, outcall_search, tenant_uuids).get_by(
        {"id": outcall_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Outcall:
    """Get an outcall by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The outcall object.

    """
    return await OutcallPersistor(session, outcall_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def find(
    session: AsyncSession, outcall_id: int, tenant_uuids: list[str] | None = None
) -> Outcall | None:
    """Find an outcall by ID.

    Args:
        session: The database session.
        outcall_id: The ID of the outcall.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The outcall object or None if not found.

    """
    return await OutcallPersistor(session, outcall_search, tenant_uuids).find_by(
        {"id": outcall_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Outcall | None:
    """Find an outcall by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The outcall object or None if not found.

    """
    return await OutcallPersistor(session, outcall_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Outcall]:
    """Find all outcalls by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of outcall objects.

    """
    result: Sequence[Outcall] = await OutcallPersistor(
        session, outcall_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, outcall: Outcall) -> Outcall:
    """Create a new outcall.

    Args:
        session: The database session.
        outcall: The outcall object to create.

    Returns:
        The created outcall object.

    """
    return await OutcallPersistor(session, outcall_search).create(outcall)


@async_daosession
async def edit(session: AsyncSession, outcall: Outcall) -> None:
    """Edit an existing outcall.

    Args:
        session: The database session.
        outcall: The outcall object to edit.

    """
    await OutcallPersistor(session, outcall_search).edit(outcall)


@async_daosession
async def delete(session: AsyncSession, outcall: Outcall) -> None:
    """Delete an outcall.

    Args:
        session: The database session.
        outcall: The outcall object to delete.

    """
    await OutcallPersistor(session, outcall_search).delete(outcall)


@async_daosession
async def associate_call_permission(
    session: AsyncSession, outcall: Outcall, call_permission: "RightCall"
) -> None:
    """Associate a call permission with an outcall.

    Args:
        session: The database session.
        outcall: The outcall object.
        call_permission: The call permission object to associate.

    """
    await OutcallPersistor(session, outcall_search).associate_call_permission(
        outcall, call_permission
    )


@async_daosession
async def dissociate_call_permission(
    session: AsyncSession, outcall: Outcall, call_permission: "RightCall"
) -> None:
    """Dissociate a call permission from an outcall.

    Args:
        session: The database session.
        outcall: The outcall object.
        call_permission: The call permission object to dissociate.

    """
    await OutcallPersistor(session, outcall_search).dissociate_call_permission(
        outcall, call_permission
    )


@async_daosession
async def associate_extension(
    session: AsyncSession, outcall: Outcall, extension: "Extension", **kwargs: Any
) -> None:
    """Associate an extension with an outcall.

    Args:
        session: The database session.
        outcall: The outcall object.
        extension: The extension object to associate.
        **kwargs: Keyword arguments for dial pattern attributes.

    """
    await OutcallPersistor(session, outcall_search).associate_extension(
        outcall, extension, **kwargs
    )


@async_daosession
async def dissociate_extension(
    session: AsyncSession, outcall: Outcall, extension: "Extension"
) -> None:
    """Dissociate an extension from an outcall.

    Args:
        session: The database session.
        outcall: The outcall object.
        extension: The extension object to dissociate.

    """
    await OutcallPersistor(session, outcall_search).dissociate_extension(
        outcall, extension
    )


@async_daosession
async def update_extension_association(
    session: AsyncSession, outcall: Outcall, extension: "Extension", **kwargs: Any
) -> None:
    """Update the association between an outcall and an extension.

    Args:
        session: The database session.
        outcall: The outcall object.
        extension: The extension object.
        **kwargs: Keyword arguments for updating dial pattern attributes.

    """
    await OutcallPersistor(session, outcall_search).update_extension_association(
        outcall, extension, **kwargs
    )
