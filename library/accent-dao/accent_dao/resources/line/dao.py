# file: accent_dao/resources/line/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.application import Application
from accent_dao.alchemy.endpoint_sip import EndpointSIP
from accent_dao.alchemy.linefeatures import LineFeatures as Line
from accent_dao.alchemy.sccpline import SCCPLine
from accent_dao.alchemy.usercustom import UserCustom
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import LinePersistor

logger = logging.getLogger(__name__)


@async_daosession
async def async_get(
    session: AsyncSession, line_id: int, tenant_uuids: list[str] | None = None
) -> Line:
    """Retrieve a line by its ID.

    Args:
        session: The database session.
        line_id: The ID of the line to retrieve.
        tenant_uuids: An optional list of tenant UUIDs to filter by.

    Returns:
        The Line object if found.  Raises NotFoundError otherwise.

    """
    return await LinePersistor(session, tenant_uuids).get_by({"id": line_id})


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Line | None:
    """Find a line by given criteria.

    Args:
        session: The database session.
        tenant_uuids: An optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments representing the criteria to filter by.

    Returns:
        The Line object if found, None otherwise.

    """
    return await LinePersistor(session, tenant_uuids).find_by(criteria)


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Line]:
    """Find all lines matching the given criteria.

    Args:
        session: The database session.
        tenant_uuids: An optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments representing the criteria to filter by.

    Returns:
        A list of Line objects.

    """
    return await LinePersistor(session, tenant_uuids).find_all_by(criteria)


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Line:
    """Get a line by given criteria.

    Args:
        session: The database session.
        tenant_uuids: An optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments representing the criteria to filter by.

    Returns:
       The Line object.

    Raises:
        NotFoundError: If no line is found that matches the criteria.

    """
    return await LinePersistor(session, tenant_uuids).get_by(criteria)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for lines based on provided parameters.

    Args:
        session: The database session.
        tenant_uuids: An optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments representing search parameters.

    Returns:
        A SearchResult object containing the total count of matching lines
        and the list of Line objects for the current page.

    """
    return await LinePersistor(session, tenant_uuids).search(parameters)


@async_daosession
async def async_create(session: AsyncSession, line: Line) -> Line:
    """Create a new line.

    Args:
        session: The database session.
        line: The Line object to create.

    Returns:
        The created Line object.

    """
    return await LinePersistor(session).create(line)


@async_daosession
async def async_edit(session: AsyncSession, line: Line) -> None:
    """Edit an existing line.

    Args:
        session: The database session.
        line: The Line object to edit.

    """
    await LinePersistor(session).edit(line)


@async_daosession
async def async_delete(session: AsyncSession, line: Line) -> None:
    """Delete a line.

    Args:
        session: The database session.
        line: The Line object to delete.

    """
    await LinePersistor(session).delete(line)


@async_daosession
async def async_associate_endpoint_sip(
    session: AsyncSession, line: Line, endpoint: EndpointSIP
) -> None:
    """Associate a SIP endpoint with a line.

    Args:
        session: The database session.
        line: The Line object.
        endpoint: The EndpointSIP object to associate.

    """
    await LinePersistor(session).associate_endpoint_sip(line, endpoint)


@async_daosession
async def async_dissociate_endpoint_sip(
    session: AsyncSession, line: Line, endpoint: EndpointSIP
) -> None:
    """Dissociate a SIP endpoint from a line.

    Args:
        session: The database session.
        line: The Line object.
        endpoint: The EndpointSIP object to dissociate.

    """
    await LinePersistor(session).dissociate_endpoint_sip(line, endpoint)


@async_daosession
async def async_associate_endpoint_sccp(
    session: AsyncSession, line: Line, endpoint: SCCPLine
) -> None:
    """Associate an SCCP endpoint with a line.

    Args:
        session: The database session.
        line: The Line object.
        endpoint: The SCCPLine object to associate.

    """
    await LinePersistor(session).associate_endpoint_sccp(line, endpoint)


@async_daosession
async def async_dissociate_endpoint_sccp(
    session: AsyncSession, line: Line, endpoint: SCCPLine
) -> None:
    """Dissociate an SCCP endpoint from a line.

    Args:
        session: The database session.
        line: The Line object.
        endpoint: The SCCPLine object to dissociate.

    """
    await LinePersistor(session).dissociate_endpoint_sccp(line, endpoint)


@async_daosession
async def async_associate_endpoint_custom(
    session: AsyncSession, line: Line, endpoint: UserCustom
) -> None:
    """Associate a custom endpoint with a line.

    Args:
        session: The database session.
        line: The Line object.
        endpoint: The UserCustom object to associate.

    """
    await LinePersistor(session).associate_endpoint_custom(line, endpoint)


@async_daosession
async def async_dissociate_endpoint_custom(
    session: AsyncSession, line: Line, endpoint: UserCustom
) -> None:
    """Dissociate a custom endpoint from a line.

    Args:
        session: The database session.
        line: The Line object.
        endpoint: The UserCustom object to dissociate.

    """
    await LinePersistor(session).dissociate_endpoint_custom(line, endpoint)


@async_daosession
async def async_associate_application(
    session: AsyncSession, line: Line, application: Application
) -> None:
    """Associate an application with a line.

    Args:
        session: The database session.
        line: The Line object.
        application: The Application object to associate.

    """
    await LinePersistor(session).associate_application(line, application)


@async_daosession
async def async_dissociate_application(
    session: AsyncSession, line: Line, application: Application
) -> None:
    """Dissociate an application from a line.

    Args:
        session: The database session.
        line: The Line object.
        application: The Application object to dissociate.

    """
    await LinePersistor(session).dissociate_application(line, application)
