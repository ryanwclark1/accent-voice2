# file: accent_dao/resources/voicemail/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.voicemail import Voicemail
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import VoicemailPersistor
from .search import voicemail_search

# Configure logging
logger = logging.getLogger(__name__)


@async_daosession
async def async_search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search for voicemails.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.

    """
    return await VoicemailPersistor(session, voicemail_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def async_get(
    session: AsyncSession, voicemail_id: int, tenant_uuids: list[str] | None = None
) -> Voicemail:
    """Get a voicemail by ID.

    Args:
        session: The database session.
        voicemail_id: The ID of the voicemail.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The voicemail.

    """
    return await VoicemailPersistor(session, voicemail_search, tenant_uuids).get_by(
        {"id": voicemail_id}
    )


@async_daosession
async def async_get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Voicemail:
    """Get a voicemail by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The voicemail.

    Raises:
        NotFoundError: If no voicemail is found with the given criteria.

    """
    return await VoicemailPersistor(session, voicemail_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def async_find(
    session: AsyncSession,
    voicemail_id: int,
    tenant_uuids: list[str] | None = None,
) -> Voicemail | None:
    """Find a voicemail by ID.

    Args:
        session: The database session.
        voicemail_id: The ID of the voicemail.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The voicemail if found, None otherwise.

    """
    return await VoicemailPersistor(session, voicemail_search, tenant_uuids).find_by(
        {"id": voicemail_id}
    )


@async_daosession
async def async_find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Voicemail | None:
    """Find a voicemail by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The voicemail if found, None otherwise.

    """
    return await VoicemailPersistor(session, voicemail_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def async_find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Voicemail]:
    """Find all voicemails by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of voicemails.

    """
    return await VoicemailPersistor(
        session, voicemail_search, tenant_uuids
    ).find_all_by(criteria)


@async_daosession
async def async_create(session: AsyncSession, voicemail: Voicemail) -> Voicemail:
    """Create a new voicemail.

    Args:
        session: The database session.
        voicemail: The voicemail to create.

    Returns:
        The created voicemail.

    """
    return await VoicemailPersistor(session, voicemail_search).create(voicemail)


@async_daosession
async def async_edit(session: AsyncSession, voicemail: Voicemail) -> None:
    """Edit an existing voicemail.

    Args:
        session: The database session.
        voicemail: The voicemail to edit.

    """
    await VoicemailPersistor(session, voicemail_search).edit(voicemail)


@async_daosession
async def async_delete(session: AsyncSession, voicemail: Voicemail) -> None:
    """Delete a voicemail.

    Args:
        session: The database session.
        voicemail: The voicemail to delete.

    """
    await VoicemailPersistor(session, voicemail_search).delete(voicemail)
