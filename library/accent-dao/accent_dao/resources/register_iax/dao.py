# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.staticiax import StaticIAX as RegisterIAX
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.register_iax.persistor import RegisterIAXPersistor
from accent_dao.resources.register_iax.search import register_iax_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, **parameters: dict
) -> "SearchResult":  # Using string literal for SearchResult
    """Search for register_iax entries.

    Args:
        session: The database session.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of register_iax entries.

    """
    return await RegisterIAXPersistor(session, register_iax_search).search(parameters)


@async_daosession
async def get(session: AsyncSession, register_iax_id: int) -> RegisterIAX:
    """Get a register_iax entry by ID.

    Args:
        session: The database session.
        register_iax_id: The ID of the register_iax entry.

    Returns:
        The RegisterIAX object.

    """
    return await RegisterIAXPersistor(session, register_iax_search).get_by(
        {"id": register_iax_id}
    )


@async_daosession
async def get_by(session: AsyncSession, **criteria: dict) -> RegisterIAX:
    """Get a register_iax entry by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The RegisterIAX object.

    """
    return await RegisterIAXPersistor(session, register_iax_search).get_by(criteria)


@async_daosession
async def find(session: AsyncSession, register_iax_id: int) -> RegisterIAX | None:
    """Find a register_iax entry by ID.

    Args:
        session: The database session.
        register_iax_id: The ID of the register_iax entry.

    Returns:
        The RegisterIAX object or None if not found.

    """
    return await RegisterIAXPersistor(session, register_iax_search).find_by(
        {"id": register_iax_id}
    )


@async_daosession
async def find_by(session: AsyncSession, **criteria: dict) -> RegisterIAX | None:
    """Find a register_iax entry by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The RegisterIAX object or None if not found.

    """
    return await RegisterIAXPersistor(session, register_iax_search).find_by(criteria)


@async_daosession
async def find_all_by(session: AsyncSession, **criteria: dict) -> list[RegisterIAX]:
    """Find all register_iax entries by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of RegisterIAX objects.

    """
    result: Sequence[RegisterIAX] = await RegisterIAXPersistor(
        session, register_iax_search
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, register: RegisterIAX) -> RegisterIAX:
    """Create a new register_iax entry.

    Args:
        session: The database session.
        register: The RegisterIAX object to create.

    Returns:
        The created RegisterIAX object.

    """
    return await RegisterIAXPersistor(session, register_iax_search).create(register)


@async_daosession
async def edit(session: AsyncSession, register: RegisterIAX) -> None:
    """Edit an existing register_iax entry.

    Args:
        session: The database session.
        register: The RegisterIAX object to edit.

    """
    await RegisterIAXPersistor(session, register_iax_search).edit(register)


@async_daosession
async def delete(session: AsyncSession, register: RegisterIAX) -> None:
    """Delete a register_iax entry.

    Args:
        session: The database session.
        register: The RegisterIAX object to delete.

    """
    await RegisterIAXPersistor(session, register_iax_search).delete(register)
