# accent_dao/tenant_dao.py
# Copyright 2025 Accent Communications

"""Tenant data access operations."""

import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from accent_dao.alchemy.tenant import Tenant
from accent_dao.helpers.db_manager import async_daosession

logger = logging.getLogger(__name__)


@async_daosession
async def find_or_create_tenant(
    session: AsyncSession, tenant_uuid: UUID | str
) -> Tenant:
    """Find an existing tenant or create a new one if it doesn't exist (async version).

    Args:
        session: The async database session.
        tenant_uuid: UUID of the tenant to find or create.

    Returns:
        The existing or newly created Tenant.

    """
    # Use SQLAlchemy 2.x async API
    tenant = await session.get(Tenant, tenant_uuid)

    if tenant:
        logger.debug("Found existing tenant with UUID: %s", tenant_uuid)
        return tenant

    tenant = Tenant(uuid=tenant_uuid)

    # Create savepoint for nested transaction
    async with session.begin_nested():
        try:
            session.add(tenant)
            await session.flush()
            logger.info("Created new tenant with UUID: %s", tenant_uuid)
        except IntegrityError:
            logger.warning("Concurrent creation of tenant with UUID: %s", tenant_uuid)
            await session.rollback()
            tenant = await session.get(Tenant, tenant_uuid)
            if tenant is None:
                msg = f"Failed to find or create tenant with UUID: {tenant_uuid}"
                raise ValueError(
                    msg
                ) from None

    return tenant


@async_daosession
async def find(session: AsyncSession) -> Tenant | None:
    """Find the first tenant in the database (async version).

    Args:
        session: The async database session.

    Returns:
        The first tenant found or None if no tenants exist.

    """
    return (await session.execute(select(Tenant).limit(1))).scalar_one_or_none()
