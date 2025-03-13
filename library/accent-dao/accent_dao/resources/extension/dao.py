# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.conference import Conference
from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.groupfeatures import GroupFeatures
from accent_dao.alchemy.incall import Incall
from accent_dao.alchemy.parking_lot import ParkingLot
from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.extension.fixes import ExtensionFixes
from accent_dao.resources.extension.persistor import ExtensionPersistor
from accent_dao.resources.extension.search import extension_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for extensions.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of extensions.

    """
    return await ExtensionPersistor(session, extension_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def get(
    session: AsyncSession, extension_id: int, tenant_uuids: list[str] | None = None
) -> Extension:
    """Get an extension by ID.

    Args:
        session: The database session.
        extension_id: The ID of the extension.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The extension object.

    """
    return await ExtensionPersistor(session, extension_search, tenant_uuids).get_by(
        {"id": extension_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Extension:
    """Get an extension by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The extension object.

    """
    return await ExtensionPersistor(session, extension_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def find(
    session: AsyncSession, extension_id: int, tenant_uuids: list[str] | None = None
) -> Extension | None:
    """Find an extension by ID.

    Args:
        session: The database session.
        extension_id: The ID of the extension.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The extension object or None if not found.

    """
    return await ExtensionPersistor(session, extension_search, tenant_uuids).find_by(
        {"id": extension_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Extension | None:
    """Find an extension by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The extension object or None if not found.

    """
    return await ExtensionPersistor(session, extension_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Extension]:
    """Find all extensions by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of extension objects.

    """
    result: Sequence[Extension] = await ExtensionPersistor(
        session, extension_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, extension: Extension) -> Extension:
    """Create a new extension.

    Args:
        session: The database session.
        extension: The extension object to create.

    Returns:
        The created extension object.

    """
    return await ExtensionPersistor(session, extension_search).create(extension)


@async_daosession
async def edit(session: AsyncSession, extension: Extension) -> None:
    """Edit an existing extension.

    Args:
        session: The database session.
        extension: The extension object to edit.

    """
    await ExtensionPersistor(session, extension_search).edit(extension)
    await ExtensionFixes(session).fix(extension.id)


@async_daosession
async def delete(session: AsyncSession, extension: Extension) -> None:
    """Delete an extension.

    Args:
        session: The database session.
        extension: The extension object to delete.

    """
    await ExtensionPersistor(session, extension_search).delete(extension)


@async_daosession
async def associate_incall(
    session: AsyncSession, incall: "Incall", extension: "Extension"
) -> None:
    """Associate an incall with an extension.

    Args:
        session: The database session.
        incall: The incall object.
        extension: The extension object.

    """
    await ExtensionPersistor(session, extension_search).associate_incall(
        incall, extension
    )
    await ExtensionFixes(session).fix(extension.id)


@async_daosession
async def dissociate_incall(
    session: AsyncSession, incall: "Incall", extension: "Extension"
) -> None:
    """Dissociate an incall from an extension.

    Args:
        session: The database session.
        incall: The incall object.
        extension: The extension object.

    """
    await ExtensionPersistor(session, extension_search).dissociate_incall(
        incall, extension
    )
    await ExtensionFixes(session).fix(extension.id)


@async_daosession
async def associate_group(
    session: AsyncSession, group: "GroupFeatures", extension: "Extension"
) -> None:
    """Associate a group with an extension.

    Args:
        session: The database session.
        group: The group object.
        extension: The extension object.

    """
    await ExtensionPersistor(session, extension_search).associate_group(
        group, extension
    )


@async_daosession
async def dissociate_group(
    session: AsyncSession, group: "GroupFeatures", extension: "Extension"
) -> None:
    """Dissociate a group from an extension.

    Args:
        session: The database session.
        group: The group object.
        extension: The extension object.

    """
    await ExtensionPersistor(session, extension_search).dissociate_group(
        group, extension
    )


@async_daosession
async def associate_queue(
    session: AsyncSession, queue: "QueueFeatures", extension: "Extension"
) -> None:
    """Associate a queue with an extension.

    Args:
        session: The database session.
        queue: The queue object.
        extension: The extension object.

    """
    await ExtensionPersistor(session, extension_search).associate_queue(
        queue, extension
    )


@async_daosession
async def dissociate_queue(
    session: AsyncSession, queue: "QueueFeatures", extension: "Extension"
) -> None:
    """Dissociate a queue from an extension.

    Args:
        session: The database session.
        queue: The queue object.
        extension: The extension object.

    """
    await ExtensionPersistor(session, extension_search).dissociate_queue(
        queue, extension
    )


@async_daosession
async def associate_conference(
    session: AsyncSession, conference: "Conference", extension: "Extension"
) -> None:
    """Associate a conference with an extension.

    Args:
        session: The database session.
        conference: The conference object.
        extension: The extension object.

    """
    await ExtensionPersistor(session, extension_search).associate_conference(
        conference, extension
    )


@async_daosession
async def dissociate_conference(
    session: AsyncSession, conference: "Conference", extension: "Extension"
) -> None:
    """Dissociate a conference from an extension.

    Args:
        session: The database session.
        conference: The conference object.
        extension: The extension object.

    """
    await ExtensionPersistor(session, extension_search).dissociate_conference(
        conference, extension
    )


@async_daosession
async def associate_parking_lot(
    session: AsyncSession, parking_lot: "ParkingLot", extension: "Extension"
) -> None:
    """Associate a parking lot with an extension.

    Args:
        session: The database session.
        parking_lot: The parking lot object.
        extension: The extension object.

    """
    await ExtensionPersistor(session, extension_search).associate_parking_lot(
        parking_lot, extension
    )


@async_daosession
async def dissociate_parking_lot(
    session: AsyncSession, parking_lot: "ParkingLot", extension: "Extension"
) -> None:
    """Dissociate a parking lot from an extension.

    Args:
        session: The database session.
        parking_lot: The parking lot object.
        extension: The extension object.

    """
    await ExtensionPersistor(session, extension_search).dissociate_parking_lot(
        parking_lot, extension
    )


@async_daosession
async def update_extension(
    session: AsyncSession, extension: "Extension", commented: int
) -> None:
    """Update the commented status of an extension.

    Args:
        session: The database session.
        extension: The extension object to update.
        commented:  Value to set.

    """
    extension.commented = commented
    await session.flush()
