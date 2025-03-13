# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.iaxcallnumberlimits import IAXCallNumberLimits
from accent_dao.helpers.db_manager import async_daosession

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


@async_daosession
async def find_all(session: AsyncSession) -> list[IAXCallNumberLimits]:
    """Retrieve all IAX call number limits.

    Args:
        session: The database session.

    Returns:
        A list of IAXCallNumberLimits objects.

    """
    stmt = select(IAXCallNumberLimits)
    result = await session.execute(stmt)
    limits = result.scalars().all()
    logger.debug("Retrieved %d IAX call number limits", len(limits))
    return list(limits)


@async_daosession
async def edit_all(
    session: AsyncSession, iax_callnumberlimits: Sequence[IAXCallNumberLimits]
) -> None:
    """Edit all IAX call number limits.

    This will replace the existing IAX call number limits with the provided ones.

    Args:
        session: The database session.
        iax_callnumberlimits: A sequence of IAXCallNumberLimits objects to update.

    """
    # Delete existing entries
    await session.execute(delete(IAXCallNumberLimits))
    # Add all IAX call number limits
    session.add_all(iax_callnumberlimits)

    logger.info("Updated all IAX call number limits")
