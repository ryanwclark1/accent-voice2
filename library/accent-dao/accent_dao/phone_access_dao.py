# file: accent_dao/dao/phone_access_dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.accessfeatures import AccessFeatures
from accent_dao.helpers.db_manager import (
    async_daosession,
    cached_query,
)

# Set up logging
logger = logging.getLogger(__name__)


@cached_query()
@async_daosession
async def get_authorized_subnets(session: AsyncSession) -> list[str]:
    """Retrieve all authorized subnets for phonebook access asynchronously.

    Args:
        session: The async database session.

    Returns:
        A list of authorized subnet host strings.

    """
    # SQLAlchemy 2.x async syntax
    stmt = select(AccessFeatures.host).where(
        and_(AccessFeatures.feature == "phonebook", AccessFeatures.commented == 0)
    )

    result = await session.execute(stmt)
    hosts = result.scalars().all()

    logger.debug("Retrieved %s authorized subnets", len(hosts))
    return list(hosts)


@async_daosession
async def add_authorized_subnet(
    session: AsyncSession, host: str
) -> AccessFeatures:
    """Add a new authorized subnet for phonebook access asynchronously.

    Args:
        session: The async database session.
        host: The host/subnet to authorize.

    Returns:
        The created AccessFeatures instance.

    """
    # Check if entry already exists
    stmt = select(AccessFeatures).where(
        and_(AccessFeatures.feature == "phonebook", AccessFeatures.host == host)
    )
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        if existing.commented == 0:
            logger.info("Subnet %s already authorized", host)
            return existing

        # If commented, enable it
        existing.enabled = True
        await session.flush()
        logger.info("Re-enabled authorized subnet %s", host)
        return existing

    # Create new entry
    access_feature = AccessFeatures(host=host, feature="phonebook", commented=0)
    session.add(access_feature)
    await session.flush()

    logger.info("Added new authorized subnet %s", host)
    return access_feature


@async_daosession
async def remove_authorized_subnet(session: AsyncSession, host: str) -> bool:
    """Remove an authorized subnet for phonebook access asynchronously.

    Args:
        session: The async database session.
        host: The host/subnet to deauthorize.

    Returns:
        True if the subnet was found and removed, False otherwise.

    """
    stmt = select(AccessFeatures).where(
        and_(AccessFeatures.feature == "phonebook", AccessFeatures.host == host)
    )
    result = await session.execute(stmt)
    access_feature = result.scalar_one_or_none()

    if not access_feature:
        logger.warning("Subnet %s not found in authorized list", host)
        return False

    # Set as commented instead of deleting
    access_feature.enabled = False
    await session.flush()

    logger.info("Removed authorized subnet %s", host)
    return True
