# file: accent_dao/resources/endpoint_custom/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from accent_dao.helpers.db_manager import async_daosession

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from accent_dao.alchemy.usercustom import UserCustom
    from accent_dao.resources.utils.search import SearchResult

from .persistor import CustomPersistor
from .search import custom_search

# Configure logging
logger = logging.getLogger(__name__)


@async_daosession
async def async_get(session: AsyncSession, custom_id: int) -> UserCustom:
    """Get a custom endpoint by ID.

    Args:
        session: The database session.
        custom_id: The ID of the custom endpoint.

    Returns:
        The custom endpoint.

    """
    return await CustomPersistor(session, custom_search).get_by({"id": custom_id})


@async_daosession
async def async_find_by(session: AsyncSession, **criteria: dict) -> UserCustom | None:
    """Find a custom endpoint by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The custom endpoint object, or None if not found.

    """
    return await CustomPersistor(session, custom_search).find_by(criteria)


@async_daosession
async def async_find_all_by(
    session: AsyncSession, **criteria: dict
) -> list[UserCustom]:
    """Find all custom endpoints by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of custom endpoint objects.

    """
    return await CustomPersistor(session, custom_search).find_all_by(criteria)


@async_daosession
async def async_search(session: AsyncSession, **parameters: dict) -> SearchResult:
    """Search for custom endpoints.

    Args:
        session: The database session.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of items.

    """
    return await CustomPersistor(session, custom_search).search(parameters)


@async_daosession
async def async_create(session: AsyncSession, custom: UserCustom) -> UserCustom:
    """Create a new custom endpoint.

    Args:
        session: The database session.
        custom: The custom endpoint object to create.

    Returns:
        The created custom endpoint object.

    """
    return await CustomPersistor(session, custom_search).create(custom)


@async_daosession
async def async_edit(session: AsyncSession, custom: UserCustom) -> None:
    """Edit an existing custom endpoint.

    Args:
        session: The database session.
        custom: The custom endpoint object to edit.

    """
    await CustomPersistor(session, custom_search).edit(custom)


@async_daosession
async def async_delete(session: AsyncSession, custom: UserCustom) -> None:
    """Delete a custom endpoint.

    Args:
        session: The database session.
        custom: The custom endpoint object to delete.

    """
    await CustomPersistor(session, custom_search).delete(custom)
