# file: accent_dao/resources/trunk/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.endpoint_sip import EndpointSIP
from accent_dao.alchemy.staticiax import StaticIAX
from accent_dao.alchemy.trunkfeatures import TrunkFeatures
from accent_dao.alchemy.usercustom import UserCustom
from accent_dao.alchemy.useriax import UserIAX
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import TrunkPersistor
from .search import trunk_search

# Configure logging
logger = logging.getLogger(__name__)


@async_daosession
async def async_get(
    session: AsyncSession, trunk_id: int, tenant_uuids: list[str] | None = None
) -> TrunkFeatures:
    """Get a trunk by ID.

    Args:
        session: The database session.
        trunk_id: The ID of the trunk.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The trunk features.

    """
    return await TrunkPersistor(session, trunk_search, tenant_uuids).get_by(
        {"id": trunk_id}
    )


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> TrunkFeatures | None:
    """Find a trunk by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The trunk features if found, None otherwise.

    """
    return await TrunkPersistor(session, trunk_search, tenant_uuids).find_by(criteria)


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[TrunkFeatures]:
    """Find all trunks by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of trunk features.

    """
    return await TrunkPersistor(session, trunk_search, tenant_uuids).find_all_by(
        criteria
    )


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> TrunkFeatures:
    """Get a trunk by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The trunk features.

    Raises:
        NotFoundError: If no trunk is found with the given criteria.

    """
    return await TrunkPersistor(session, trunk_search, tenant_uuids).get_by(criteria)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for trunks.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of items.

    """
    return await TrunkPersistor(session, trunk_search, tenant_uuids).search(parameters)


@async_daosession
async def async_create(session: AsyncSession, trunk: TrunkFeatures) -> TrunkFeatures:
    """Create a new trunk.

    Args:
        session: The database session.
        trunk: The trunk to create.

    Returns:
        The created trunk.

    """
    return await TrunkPersistor(session, trunk_search).create(trunk)


@async_daosession
async def async_edit(session: AsyncSession, trunk: TrunkFeatures) -> None:
    """Edit an existing trunk.

    Args:
        session: The database session.
        trunk: The trunk to edit.

    """
    await TrunkPersistor(session, trunk_search).edit(trunk)


@async_daosession
async def async_delete(session: AsyncSession, trunk: TrunkFeatures) -> None:
    """Delete a trunk.

    Args:
        session: The database session.
        trunk: The trunk to delete.

    """
    await TrunkPersistor(session, trunk_search).delete(trunk)


@async_daosession
async def async_associate_endpoint_sip(
    session: AsyncSession, trunk: TrunkFeatures, endpoint: EndpointSIP
) -> None:
    """Associate a SIP endpoint with a trunk.

    Args:
        session: The database session.
        trunk: The trunk to associate.
        endpoint: The SIP endpoint to associate.

    """
    await TrunkPersistor(session, trunk_search).associate_endpoint_sip(trunk, endpoint)


@async_daosession
async def async_dissociate_endpoint_sip(
    session: AsyncSession, trunk: TrunkFeatures, endpoint: EndpointSIP
) -> None:
    """Dissociate a SIP endpoint from a trunk.

    Args:
        session: The database session.
        trunk: The trunk to dissociate.
        endpoint: The SIP endpoint to dissociate.

    """
    await TrunkPersistor(session, trunk_search).dissociate_endpoint_sip(trunk, endpoint)


@async_daosession
async def async_associate_endpoint_iax(
    session: AsyncSession, trunk: TrunkFeatures, endpoint: UserIAX
) -> None:
    """Associate an IAX endpoint with a trunk.

    Args:
        session: The database session.
        trunk: The trunk to associate.
        endpoint: The IAX endpoint to associate.

    """
    await TrunkPersistor(session, trunk_search).associate_endpoint_iax(trunk, endpoint)


@async_daosession
async def async_dissociate_endpoint_iax(
    session: AsyncSession, trunk: TrunkFeatures, endpoint: UserIAX
) -> None:
    """Dissociate an IAX endpoint from a trunk.

    Args:
        session: The database session.
        trunk: The trunk to dissociate.
        endpoint: The IAX endpoint to dissociate.

    """
    await TrunkPersistor(session, trunk_search).dissociate_endpoint_iax(trunk, endpoint)


@async_daosession
async def async_associate_endpoint_custom(
    session: AsyncSession, trunk: TrunkFeatures, endpoint: UserCustom
) -> None:
    """Associate a custom endpoint with a trunk.

    Args:
        session: The database session.
        trunk: The trunk to associate.
        endpoint: The custom endpoint to associate.

    """
    await TrunkPersistor(session, trunk_search).associate_endpoint_custom(
        trunk, endpoint
    )


@async_daosession
async def async_dissociate_endpoint_custom(
    session: AsyncSession, trunk: TrunkFeatures, endpoint: UserCustom
) -> None:
    """Dissociate a custom endpoint from a trunk.

    Args:
        session: The database session.
        trunk: The trunk to dissociate.
        endpoint: The custom endpoint to dissociate.

    """
    await TrunkPersistor(session, trunk_search).dissociate_endpoint_custom(
        trunk, endpoint
    )


@async_daosession
async def async_associate_register_iax(
    session: AsyncSession, trunk: TrunkFeatures, register: StaticIAX
) -> None:
    """Associate a register IAX with a trunk.

    Args:
        session: The database session.
        trunk: The trunk to associate.
        register: The register IAX to associate.

    """
    await TrunkPersistor(session, trunk_search).associate_register_iax(trunk, register)


@async_daosession
async def async_dissociate_register_iax(
    session: AsyncSession, trunk: TrunkFeatures, register: StaticIAX
) -> None:
    """Dissociate a register IAX from a trunk.

    Args:
        session: The database session.
        trunk: The trunk to dissociate.
        register: The register IAX to dissociate.

    """
    await TrunkPersistor(session, trunk_search).dissociate_register_iax(trunk, register)
