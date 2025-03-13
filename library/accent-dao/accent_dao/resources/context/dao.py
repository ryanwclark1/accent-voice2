# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.context import Context
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.context.persistor import ContextPersistor
from accent_dao.resources.context.search import context_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for contexts.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of contexts.

    """
    return await ContextPersistor(session, context_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def get(
    session: AsyncSession, context_id: int, tenant_uuids: list[str] | None = None
) -> Context:
    """Get a context by ID.

    Args:
        session: The database session.
        context_id: The ID of the context.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The context object.

    """
    return await ContextPersistor(session, context_search, tenant_uuids).get_by(
        {"id": context_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Context:
    """Get a context by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The context object.

    """
    return await ContextPersistor(session, context_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def get_by_name(
    session: AsyncSession, context_name: str, tenant_uuids: list[str] | None = None
) -> Context:
    """Get a context by name.

    Args:
        session: The database session.
        context_name: The name of the context.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The context object.

    """
    return await ContextPersistor(session, context_search, tenant_uuids).get_by(
        {"name": context_name}
    )


@async_daosession
async def find(
    session: AsyncSession, context_id: int, tenant_uuids: list[str] | None = None
) -> Context | None:
    """Find a context by ID.

    Args:
        session: The database session.
        context_id: The ID of the context.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The context object or None if not found.

    """
    return await ContextPersistor(session, context_search, tenant_uuids).find_by(
        {"id": context_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Context | None:
    """Find a context by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The context object or None if not found.

    """
    return await ContextPersistor(session, context_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[Context]:
    """Find all contexts by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of context objects.

    """
    result: Sequence[Context] = await ContextPersistor(
        session, context_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, context: Context) -> Context:
    """Create a new context.

    Args:
        session: The database session.
        context: The context object to create.

    Returns:
        The created context object.

    """
    return await ContextPersistor(session, context_search).create(context)


@async_daosession
async def edit(session: AsyncSession, context: Context) -> None:
    """Edit an existing context.

    Args:
        session: The database session.
        context: The context object to edit.

    """
    await ContextPersistor(session, context_search).edit(context)


@async_daosession
async def delete(session: AsyncSession, context: Context) -> None:
    """Delete a context.

    Args:
        session: The database session.
        context: The context object to delete.

    """
    await ContextPersistor(session, context_search).delete(context)


@async_daosession
async def associate_contexts(
    session: AsyncSession, context: Context, contexts: list[str]
) -> None:
    """Associate included contexts with a context.

    Args:
        session: The database session.
        context: The context object.
        contexts: List of included context

    """
    await ContextPersistor(session, context_search).associate_contexts(
        context, contexts
    )
