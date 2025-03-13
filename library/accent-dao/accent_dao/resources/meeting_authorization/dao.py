# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.meeting_authorization import MeetingAuthorization
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.meeting_authorization.persistor import (
    MeetingAuthorizationPersistor,
)
from accent_dao.resources.meeting_authorization.search import (
    meeting_authorization_search,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, meeting_uuid: str | None, **parameters: dict
) -> "SearchResult":
    """Search for meeting authorizations.

    Args:
        session: The database session.
        meeting_uuid: The meeting's UUID.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of authorizations.

    """
    return await MeetingAuthorizationPersistor(
        session, meeting_authorization_search, meeting_uuid
    ).search(parameters)


@async_daosession
async def get(
    session: AsyncSession,
    meeting_uuid: str | None,
    authorization_uuid: str,
    **criteria: dict,
) -> MeetingAuthorization:
    """Get a meeting authorization by UUID.

    Args:
        session: The database session.
        meeting_uuid: The meeting's UUID.
        authorization_uuid: The authorization's UUID.
        **criteria: Keyword arguments for filtering.

    Returns:
        The meeting authorization object.

    """
    criteria["uuid"] = authorization_uuid
    return await MeetingAuthorizationPersistor(
        session, meeting_authorization_search, meeting_uuid
    ).get_by(criteria)


@async_daosession
async def get_by(
    session: AsyncSession, meeting_uuid: str | None, **criteria: dict
) -> MeetingAuthorization:
    """Get a meeting authorization by criteria.

    Args:
        session: The database session.
        meeting_uuid: The meeting's UUID.
        **criteria: Keyword arguments for filtering.

    Returns:
        The meeting authorization object.

    """
    return await MeetingAuthorizationPersistor(
        session, meeting_authorization_search, meeting_uuid
    ).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession,
    meeting_uuid: str | None,
    authorization_uuid: str,
    **criteria: dict,
) -> MeetingAuthorization | None:
    """Find a meeting authorization by UUID.

    Args:
        session: The database session.
        meeting_uuid: The meeting's UUID.
        authorization_uuid: The authorization's UUID.
        **criteria: Keyword arguments for filtering.

    Returns:
        The meeting authorization object, or None if not found.

    """
    criteria["uuid"] = authorization_uuid
    return await MeetingAuthorizationPersistor(
        session, meeting_authorization_search, meeting_uuid
    ).find_by(criteria)


@async_daosession
async def find_by(
    session: AsyncSession, meeting_uuid: str | None, **criteria: dict
) -> MeetingAuthorization | None:
    """Find a meeting authorization by criteria.

    Args:
        session: The database session.
        meeting_uuid: The meeting's UUID.
        **criteria: Keyword arguments for filtering.

    Returns:
        The meeting authorization object, or None if not found.

    """
    return await MeetingAuthorizationPersistor(
        session, meeting_authorization_search, meeting_uuid
    ).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, meeting_uuid: str | None, **criteria: dict
) -> list[MeetingAuthorization]:
    """Find all meeting authorizations by criteria.

    Args:
        session: The database session.
        meeting_uuid: The meeting's UUID.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of meeting authorization objects.

    """
    result: Sequence[MeetingAuthorization] = await MeetingAuthorizationPersistor(
        session, meeting_authorization_search, meeting_uuid
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(
    session: AsyncSession, meeting_authorization: MeetingAuthorization
) -> MeetingAuthorization:
    """Create a new meeting authorization.

    Args:
        session: The database session.
        meeting_authorization: The meeting authorization object to create.

    Returns:
        The created meeting authorization object.

    """
    return await MeetingAuthorizationPersistor(
        session, meeting_authorization_search
    ).create(meeting_authorization)


@async_daosession
async def edit(
    session: AsyncSession, meeting_authorization: MeetingAuthorization
) -> None:
    """Edit an existing meeting authorization.

    Args:
        session: The database session.
        meeting_authorization: The meeting authorization object to edit.

    """
    await MeetingAuthorizationPersistor(session, meeting_authorization_search).edit(
        meeting_authorization
    )


@async_daosession
async def delete(
    session: AsyncSession, meeting_authorization: MeetingAuthorization
) -> None:
    """Delete a meeting authorization.

    Args:
        session: The database session.
        meeting_authorization: The meeting authorization object to delete.

    """
    await MeetingAuthorizationPersistor(session, meeting_authorization_search).delete(
        meeting_authorization
    )
