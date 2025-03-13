# file: accent_dao/dao/context_dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from accent_dao.alchemy.context import Context
from accent_dao.helpers.db_manager import (
    async_daosession,
    cached_query,
    daosession,
)

# Set up logging
logger = logging.getLogger(__name__)


@daosession
def get(session: Session, context_name: str) -> Context | None:
    """Retrieve a context by its name.

    Args:
        session: The database session.
        context_name: The name of the context to retrieve.

    Returns:
        The context if found, None otherwise.

    """
    # Updated for SQLAlchemy 2.x syntax
    stmt = select(Context).where(Context.name == context_name)
    result = session.execute(stmt).scalar_one_or_none()

    if result:
        logger.debug("Retrieved context with name %s", context_name)
    else:
        logger.debug("Context with name %s not found", context_name)

    return result


@cached_query()
@async_daosession
async def async_get(session: AsyncSession, context_name: str) -> Context | None:
    """Retrieve a context by its name asynchronously.

    Args:
        session: The async database session.
        context_name: The name of the context to retrieve.

    Returns:
        The context if found, None otherwise.

    """
    # SQLAlchemy 2.x async syntax
    stmt = select(Context).where(Context.name == context_name)
    result = await session.execute(stmt)
    context = result.scalar_one_or_none()

    if context:
        logger.debug("Retrieved context with name %s", context_name)
    else:
        logger.debug("Context with name %s not found", context_name)

    return context


@daosession
def get_by_uuid(session: Session, context_uuid: str) -> Context | None:
    """Retrieve a context by its UUID.

    Args:
        session: The database session.
        context_uuid: The UUID of the context to retrieve.

    Returns:
        The context if found, None otherwise.

    """
    stmt = select(Context).where(Context.uuid == context_uuid)
    result = session.execute(stmt).scalar_one_or_none()

    if result:
        logger.debug("Retrieved context with UUID %s", context_uuid)
    else:
        logger.debug("Context with UUID %s not found", context_uuid)

    return result


@cached_query()
@async_daosession
async def async_get_by_uuid(
    session: AsyncSession, context_uuid: str
) -> Context | None:
    """Retrieve a context by its UUID asynchronously.

    Args:
        session: The async database session.
        context_uuid: The UUID of the context to retrieve.

    Returns:
        The context if found, None otherwise.

    """
    stmt = select(Context).where(Context.uuid == context_uuid)
    result = await session.execute(stmt)
    context = result.scalar_one_or_none()

    if context:
        logger.debug("Retrieved context with UUID %s", context_uuid)
    else:
        logger.debug("Context with UUID %s not found", context_uuid)

    return context


@daosession
def get_all(
    session: Session, tenant_uuid: str | list[str] | None = None
) -> list[Context]:
    """Retrieve all contexts, optionally filtered by tenant UUID.

    Args:
        session: The database session.
        tenant_uuid: Optional tenant UUID or list of UUIDs to filter by.

    Returns:
        A list of contexts.

    """
    stmt = select(Context)

    if tenant_uuid is not None:
        if isinstance(tenant_uuid, str):
            stmt = stmt.where(Context.tenant_uuid == tenant_uuid)
        else:
            stmt = stmt.where(Context.tenant_uuid.in_(tenant_uuid))

    result = session.execute(stmt)
    contexts = result.scalars().all()

    logger.info("Retrieved %s contexts", len(contexts))
    return list(contexts)


@async_daosession
async def async_get_all(
    session: AsyncSession, tenant_uuid: str | list[str] | None = None
) -> list[Context]:
    """Retrieve all contexts asynchronously, optionally filtered by tenant UUID.

    Args:
        session: The async database session.
        tenant_uuid: Optional tenant UUID or list of UUIDs to filter by.

    Returns:
        A list of contexts.

    """
    stmt = select(Context)

    if tenant_uuid is not None:
        if isinstance(tenant_uuid, str):
            stmt = stmt.where(Context.tenant_uuid == tenant_uuid)
        else:
            stmt = stmt.where(Context.tenant_uuid.in_(tenant_uuid))

    result = await session.execute(stmt)
    contexts = result.scalars().all()

    logger.info("Retrieved %s contexts", len(contexts))
    return list(contexts)


@daosession
def create(  # noqa: PLR0913
    session: Session,
    name: str,
    tenant_uuid: str,
    label: str | None = None,
    type_val: str = "internal",
    description: str | None = None,
    enabled: bool = True,
) -> Context:
    """Create a new context.

    Args:
        session: The database session.
        name: The name of the context.
        tenant_uuid: The UUID of the tenant.
        label: Optional display name for the context.
        type_val: The type of the context (default: 'internal').
        description: Optional description of the context.
        enabled: Whether the context is enabled (default: True).

    Returns:
        The created context.

    """
    context = Context(
        name=name,
        tenant_uuid=tenant_uuid,
        displayname=label,
        contexttype=type_val,
        description=description,
        commented=int(not enabled),
    )

    session.add(context)
    session.flush()

    logger.info("Created new context %s", name)
    return context


@async_daosession
async def async_create(  # noqa: PLR0913
    session: AsyncSession,
    name: str,
    tenant_uuid: str,
    label: str | None = None,
    type_val: str = "internal",
    description: str | None = None,
    enabled: bool = True,
) -> Context:
    """Create a new context asynchronously.

    Args:
        session: The async database session.
        name: The name of the context.
        tenant_uuid: The UUID of the tenant.
        label: Optional display name for the context.
        type_val: The type of the context (default: 'internal').
        description: Optional description of the context.
        enabled: Whether the context is enabled (default: True).

    Returns:
        The created context.

    """
    context = Context(
        name=name,
        tenant_uuid=tenant_uuid,
        displayname=label,
        contexttype=type_val,
        description=description,
        commented=int(not enabled),
    )

    session.add(context)
    await session.flush()

    logger.info("Created new context %s", name)
    return context
