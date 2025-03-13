# file: accent_dao/resources/extension/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.extension import Extension
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .fixes import ExtensionFixes
from .persistor import ExtensionPersistor

# Set up logging
logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for extensions.

    Args:
        session: Database session.
        tenant_uuids: Optional list of tenant UUIDs.
        parameters: Search parameters.

    Returns:
        SearchResult: Search results.

    """
    return await ExtensionPersistor(session, tenant_uuids).search(parameters)


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Extension:
    """Get an extension by criteria.

    Args:
        session: Database session.
        tenant_uuids: Optional list of tenant UUIDs.
        criteria: Filter criteria.

    Returns:
        The extension.

    """
    return await ExtensionPersistor(session, tenant_uuids).get_by(criteria)


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Extension | None:
    """Find an extension by criteria.

    Args:
        session: Database session.
        tenant_uuids: Optional list of tenant UUIDs.
        criteria: Filter criteria.

    Returns:
        The extension or None.

    """
    return await ExtensionPersistor(session, tenant_uuids).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Extension]:
    """Find all extensions by criteria.

    Args:
        session: Database session.
        tenant_uuids: Optional list of tenant UUIDs.
        criteria: Filter criteria.

    Returns:
        A list of extensions.

    """
    return await ExtensionPersistor(session, tenant_uuids).find_all_by(criteria)


@async_daosession
async def get(
    session: AsyncSession, id: int, tenant_uuids: list[str] | None = None
) -> Extension:
    """Get an extension by ID.

    Args:
        session: Database session.
        id: Extension ID.
        tenant_uuids: Optional list of tenant UUIDs.

    Returns:
        The extension.

    """
    return await ExtensionPersistor(session, tenant_uuids).get_by({"id": id})


@async_daosession
async def find(
    session: AsyncSession, id: int, tenant_uuids: list[str] | None = None
) -> Extension | None:
    """Find an extension by ID.

    Args:
        session: Database session.
        id: Extension ID.
        tenant_uuids: Optional list of tenant UUIDs.

    Returns:
        The extension or None.

    """
    return await ExtensionPersistor(session, tenant_uuids).find_by({"id": id})


@async_daosession
async def create(session: AsyncSession, extension: Extension) -> Extension:
    """Create a new extension.

    Args:
        session: Database session.
        extension: Extension to create.

    Returns:
        The created extension.

    """
    return await ExtensionPersistor(session).create(extension)


@async_daosession
async def edit(session: AsyncSession, extension: Extension) -> None:
    """Edit an existing extension.

    Args:
        session: Database session.
        extension: Extension to edit.

    """
    await ExtensionPersistor(session).edit(extension)
    await ExtensionFixes(session).async_fix(extension.id)


@async_daosession
async def delete(session: AsyncSession, extension: Extension) -> None:
    """Delete an extension.

    Args:
        session: Database session.
        extension: Extension to delete.

    """
    await ExtensionPersistor(session).delete(extension)


@async_daosession
async def associate_incall(
    session: AsyncSession, incall: Any, extension: Extension
) -> None:
    """Associate an incall with an extension.

    Args:
        session: Database session.
        incall: Inbound call.
        extension: Extension.

    """
    await ExtensionPersistor(session).associate_incall(incall, extension)
    await ExtensionFixes(session).async_fix(extension.id)


@async_daosession
async def dissociate_incall(
    session: AsyncSession, incall: Any, extension: Extension
) -> None:
    """Dissociate an incall from an extension.

    Args:
        session: Database session.
        incall: Inbound call.
        extension: Extension.

    """
    await ExtensionPersistor(session).dissociate_incall(incall, extension)
    await ExtensionFixes(session).async_fix(extension.id)


@async_daosession
async def associate_group(
    session: AsyncSession, group: Any, extension: Extension
) -> None:
    """Associate a group with an extension.

    Args:
        session: Database session.
        group: Group.
        extension: Extension.

    """
    await ExtensionPersistor(session).associate_group(group, extension)


@async_daosession
async def dissociate_group(
    session: AsyncSession, group: Any, extension: Extension
) -> None:
    """Dissociate a group from an extension.

    Args:
        session: Database session.
        group: Group.
        extension: Extension.

    """
    await ExtensionPersistor(session).dissociate_group(group, extension)


@async_daosession
async def associate_queue(
    session: AsyncSession, queue: Any, extension: Extension
) -> None:
    """Associate a queue with an extension.

    Args:
        session: Database session.
        queue: Queue.
        extension: Extension.

    """
    await ExtensionPersistor(session).associate_queue(queue, extension)


@async_daosession
async def dissociate_queue(
    session: AsyncSession, queue: Any, extension: Extension
) -> None:
    """Dissociate a queue from an extension.

    Args:
        session: Database session.
        queue: Queue.
        extension: Extension.

    """
    await ExtensionPersistor(session).dissociate_queue(queue, extension)


@async_daosession
async def associate_conference(
    session: AsyncSession, conference: Any, extension: Extension
) -> None:
    """Associate a conference with an extension.

    Args:
        session: Database session.
        conference: Conference.
        extension: Extension.

    """
    await ExtensionPersistor(session).associate_conference(conference, extension)


@async_daosession
async def dissociate_conference(
    session: AsyncSession, conference: Any, extension: Extension
) -> None:
    """Dissociate a conference from an extension.

    Args:
        session: Database session.
        conference: Conference.
        extension: Extension.

    """
    await ExtensionPersistor(session).dissociate_conference(conference, extension)


@async_daosession
async def associate_parking_lot(
    session: AsyncSession, parking_lot: Any, extension: Extension
) -> None:
    """Associate a parking lot with an extension.

    Args:
        session: Database session.
        parking_lot: Parking lot.
        extension: Extension.

    """
    await ExtensionPersistor(session).associate_parking_lot(parking_lot, extension)


@async_daosession
async def dissociate_parking_lot(
    session: AsyncSession, parking_lot: Any, extension: Extension
) -> None:
    """Dissociate a parking lot from an extension.

    Args:
        session: Database session.
        parking_lot: Parking lot.
        extension: Extension.

    """
    await ExtensionPersistor(session).dissociate_parking_lot(parking_lot, extension)
