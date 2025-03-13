# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.infos import Infos
from accent_dao.helpers.db_manager import async_daosession

logger = logging.getLogger(__name__)


@async_daosession
async def get(session: AsyncSession) -> Infos:
    """Retrieve the system information.

    Args:
        session: The database session.

    Returns:
        The Infos object.

    Raises:
        LookupError: if there are no configuration.

    """
    stmt = select(Infos)
    result = await session.execute(stmt)
    infos = result.scalar_one_or_none()

    if not infos:
        logger.error("Infos table is empty")
        raise LookupError("Infos configuration not found")

    return infos


@async_daosession
async def set_live_reload_status(session: AsyncSession, data: dict) -> None:
    """Set the live reload status.

    Args:
        session: The database session.
        data: A dictionary containing the 'enabled' key with a boolean value.

    """
    value = data["enabled"]
    # Use SQLAlchemy's update for a cleaner approach
    await session.execute(update(Infos).values(live_reload_enabled=value))
    logger.info("Live reload status set to: %s", value)
