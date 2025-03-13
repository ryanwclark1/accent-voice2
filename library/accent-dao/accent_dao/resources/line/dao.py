# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.line.persistor import LinePersistor
from accent_dao.resources.line.search import line_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.alchemy.application import Application
    from accent_dao.alchemy.endpoint_sip import EndpointSIP
    from accent_dao.alchemy.sccpline import SCCPLine
    from accent_dao.alchemy.usercustom import UserCustom
    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for lines.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of lines.

    """
    return await LinePersistor(session, line_search, tenant_uuids).search(parameters)


@async_daosession
async def get(
    session: AsyncSession, line_id: int, tenant_uuids: list[str] | None = None
) -> LineFeatures:
    """Get a line by ID.

    Args:
        session: The database session.
        line_id: The ID of the line.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The line object.

    """
    return await LinePersistor(session, line_search, tenant_uuids).get_by(
        {"id": line_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> LineFeatures:
    """Get a line by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The line object.

    """
    return await LinePersistor(session, line_search, tenant_uuids).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession, line_id: int, tenant_uuids: list[str] | None = None
) -> LineFeatures | None:
    """Find a line by ID.

    Args:
        session: The database session.
        line_id: The ID of the line.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The line object or None if not found.

    """
    return await LinePersistor(session, line_search, tenant_uuids).find_by(
        {"id": line_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> LineFeatures | None:
    """Find a line by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The line object or None if not found.

    """
    return await LinePersistor(session, line_search, tenant_uuids).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[LineFeatures]:
    """Find all lines by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of line objects.

    """
    result: Sequence[LineFeatures] = await LinePersistor(
        session, line_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, line: LineFeatures) -> LineFeatures:
    """Create a new line.

    Args:
        session: The database session.
        line: The line object to create.

    Returns:
        The created line object.

    """
    return await LinePersistor(session, line_search).create(line)


@async_daosession
async def edit(session: AsyncSession, line: LineFeatures) -> None:
    """Edit an existing line.

    Args:
        session: The database session.
        line: The line object to edit.

    """
    await LinePersistor(session, line_search).edit(line)


@async_daosession
async def delete(session: AsyncSession, line: LineFeatures) -> None:
    """Delete a line.

    Args:
        session: The database session.
        line: The line object to delete.

    """
    await LinePersistor(session, line_search).delete(line)


@async_daosession
async def associate_endpoint_sip(
    session: AsyncSession, line: LineFeatures, endpoint: "EndpointSIP"
) -> None:
    """Associate a SIP endpoint with a line.

    Args:
        session: The database session.
        line: The line object.
        endpoint: The SIP endpoint object to associate.

    """
    await LinePersistor(session, line_search).associate_endpoint_sip(line, endpoint)


@async_daosession
async def dissociate_endpoint_sip(
    session: AsyncSession, line: LineFeatures, endpoint: "EndpointSIP"
) -> None:
    """Dissociate a SIP endpoint from a line.

    Args:
        session: The database session.
        line: The line object.
        endpoint: The SIP endpoint object to dissociate.

    """
    await LinePersistor(session, line_search).dissociate_endpoint_sip(line, endpoint)


@async_daosession
async def associate_endpoint_sccp(
    session: AsyncSession, line: LineFeatures, endpoint: "SCCPLine"
) -> None:
    """Associate an SCCP endpoint with a line.

    Args:
        session: The database session.
        line: The line object.
        endpoint: The SCCP endpoint object to associate.

    """
    await LinePersistor(session, line_search).associate_endpoint_sccp(line, endpoint)


@async_daosession
async def dissociate_endpoint_sccp(
    session: AsyncSession, line: LineFeatures, endpoint: "SCCPLine"
) -> None:
    """Dissociate an SCCP endpoint from a line.

    Args:
        session: The database session.
        line: The line object.
        endpoint: The SCCP endpoint object to dissociate.

    """
    await LinePersistor(session, line_search).dissociate_endpoint_sccp(line, endpoint)


@async_daosession
async def associate_endpoint_custom(
    session: AsyncSession, line: LineFeatures, endpoint: "UserCustom"
) -> None:
    """Associate a custom endpoint with a line.

    Args:
        session: The database session.
        line: The line object.
        endpoint: The custom endpoint object to associate.

    """
    await LinePersistor(session, line_search).associate_endpoint_custom(line, endpoint)


@async_daosession
async def dissociate_endpoint_custom(
    session: AsyncSession, line: LineFeatures, endpoint: "UserCustom"
) -> None:
    """Dissociate a custom endpoint from a line.

    Args:
        session: The database session.
        line: The line object.
        endpoint: The custom endpoint object to dissociate.

    """
    await LinePersistor(session, line_search).dissociate_endpoint_custom(line, endpoint)


@async_daosession
async def associate_application(
    session: AsyncSession, line: LineFeatures, application: "Application"
) -> None:
    """Associate an application with a line.

    Args:
        session: The database session.
        line: The line object.
        application: The application object to associate.

    """
    await LinePersistor(session, line_search).associate_application(line, application)


@async_daosession
async def dissociate_application(
    session: AsyncSession, line: LineFeatures, application: "Application"
) -> None:
    """Dissociate an application from a line.

    Args:
        session: The database session.
        line: The line object.
        application: The application object to dissociate.

    """
    await LinePersistor(session, line_search).dissociate_application(line, application)
