# file: accent_dao/resources/context/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.context import Context
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.context.persistor import ContextPersistor

# Configure logging
logger = logging.getLogger(__name__)


@async_daosession
async def get(session: AsyncSession, context_name: str) -> Context | None:
    """Retrieve a context by its name.

    Args:
        session: The database session.
        context_name: The name of the context to retrieve.

    Returns:
        The context if found, None otherwise.

    """
    return await ContextPersistor(session).find_by(name=context_name)


@async_daosession
async def get_by_uuid(session: AsyncSession, context_uuid: str) -> Context | None:
    """Retrieve a context by its UUID.

    Args:
        session: The database session.
        context_uuid: The UUID of the context to retrieve.

    Returns:
        The context if found, None otherwise.

    """
    return await ContextPersistor(session).find_by(uuid=context_uuid)


@async_daosession
async def get_all(
    session: AsyncSession, tenant_uuid: str | list[str] | None = None
) -> list[Context]:
    """Retrieve all contexts, optionally filtered by tenant UUID.

    Args:
        session: The database session.
        tenant_uuid: Optional tenant UUID or list of UUIDs to filter by.

    Returns:
        A list of contexts.

    """
    return await ContextPersistor(session, tenant_uuids=tenant_uuid).find_all_by()


@async_daosession
async def create(session: AsyncSession, context: Context) -> Context:
    """Create a new context.

    Args:
        session: The database session.
        context: The context object to create.

    Returns:
        The created context object.

    """
    return await ContextPersistor(session).create(context)


@async_daosession
async def edit(session: AsyncSession, context: Context) -> None:
    """Edit an existing context.

    Args:
        session: The database session.
        context: The context object to edit.

    """
    await ContextPersistor(session).edit(context)


@async_daosession
async def delete(session: AsyncSession, context: Context) -> None:
    """Delete a context.

    Args:
        session: The database session.
        context: The context object to delete.

    """
    await ContextPersistor(session).delete(context)


@async_daosession
async def associate_contexts(
    session: AsyncSession, context: Context, contexts: list[str]
) -> None:
    """Associate a list of contexts with a context.

    Args:
        session: The database session.
        context: The context to associate with.
        contexts: A list of contexts to associate.

    """
    await ContextPersistor(session).associate_contexts(context, contexts)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> list[Context]:
    """Search the contexts by provided parameters.

    Args:
        session: The database session.
        tenant_uuid: Optional tenant UUID or list of UUIDs to filter by.

    Returns:
        A list of context objects.

    """
    return await ContextPersistor(session, tenant_uuids=tenant_uuids).search(parameters)


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Context | None:
    """Find all contexts by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        list[Context]: A list of context objects.

    """
    return await ContextPersistor(session, tenant_uuids=tenant_uuids).find_by(
        **criteria
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> Context:
    """Get all contexts by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        list[Context]: A list of context objects.

    """
    return await ContextPersistor(session, tenant_uuids=tenant_uuids).get_by(**criteria)


@async_daosession
async def find(
    session: AsyncSession, context_id: int, tenant_uuids: list[str] | None = None
) -> Context | None:
    """Find context instance by id.

    Args:
        session: The database session.
        context_id: Context id.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        Context | None : The context, or None if not found.

    """
    return await ContextPersistor(session, tenant_uuids=tenant_uuids).find_by(
        id=context_id
    )
