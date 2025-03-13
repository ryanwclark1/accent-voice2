# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.pjsip_transport import PJSIPTransport
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.pjsip_transport.persistor import PJSIPTransportPersistor
from accent_dao.resources.pjsip_transport.search import transport_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(session: AsyncSession, **parameters: dict) -> "SearchResult":
    """Search for PJSIP transports.

    Args:
        session: The database session.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of PJSIP transports.

    """
    return await PJSIPTransportPersistor(session, transport_search).search(parameters)


@async_daosession
async def get(session: AsyncSession, transport_uuid: str) -> PJSIPTransport:
    """Get a PJSIP transport by UUID.

    Args:
        session: The database session.
        transport_uuid: The UUID of the PJSIP transport.

    Returns:
        The PJSIPTransport object.

    """
    return await PJSIPTransportPersistor(session, transport_search).get_by(
        {"uuid": transport_uuid}
    )


@async_daosession
async def get_by(session: AsyncSession, **criteria: dict) -> PJSIPTransport:
    """Get a PJSIP transport by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The PJSIPTransport object.

    """
    return await PJSIPTransportPersistor(session, transport_search).get_by(criteria)


@async_daosession
async def find(session: AsyncSession, transport_uuid: str) -> PJSIPTransport | None:
    """Find a PJSIP transport by UUID.

    Args:
        session: The database session.
        transport_uuid: The UUID of the PJSIP transport.

    Returns:
        The PJSIPTransport object or None if not found.

    """
    return await PJSIPTransportPersistor(session, transport_search).find_by(
        {"uuid": transport_uuid}
    )


@async_daosession
async def find_by(session: AsyncSession, **criteria: dict) -> PJSIPTransport | None:
    """Find a PJSIP transport by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The PJSIPTransport object or None if not found.

    """
    return await PJSIPTransportPersistor(session, transport_search).find_by(criteria)


@async_daosession
async def find_all_by(session: AsyncSession, **criteria: dict) -> list[PJSIPTransport]:
    """Find all PJSIP transports by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of PJSIPTransport objects.

    """
    result: Sequence[PJSIPTransport] = await PJSIPTransportPersistor(
        session, transport_search
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, transport: PJSIPTransport) -> PJSIPTransport:
    """Create a new PJSIP transport.

    Args:
        session: The database session.
        transport: The PJSIPTransport object to create.

    Returns:
        The created PJSIPTransport object.

    """
    return await PJSIPTransportPersistor(session, transport_search).create(transport)


@async_daosession
async def edit(session: AsyncSession, transport: PJSIPTransport) -> None:
    """Edit an existing PJSIP transport.

    Args:
        session: The database session.
        transport: The PJSIPTransport object to edit.

    """
    await PJSIPTransportPersistor(session, transport_search).edit(transport)


@async_daosession
async def delete(
    session: AsyncSession,
    transport: PJSIPTransport,
    fallback: PJSIPTransport | None = None,
) -> None:
    """Delete a PJSIP transport.

    Args:
        session: The database session.
        transport: The PJSIPTransport object to delete.
        fallback: An optional fallback transport to reassign endpoints to.

    """
    await PJSIPTransportPersistor(session, transport_search).delete(transport, fallback)
