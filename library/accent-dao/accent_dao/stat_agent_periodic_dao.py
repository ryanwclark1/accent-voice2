# file: accent_dao/stat_agent_periodic_dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

"""Data access operations for StatAgentPeriodic entities."""

import logging
from datetime import datetime

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.stat_agent_periodic import StatAgentPeriodic
from accent_dao.helpers.db_manager import async_daosession

logger = logging.getLogger(__name__)



@async_daosession
async def insert_stats(
    session: AsyncSession,
    period_stats: dict[int, dict[str, str]],
    period_start: datetime,
) -> None:
    """Insert agent periodic statistics asynchronously.

    Args:
        session: The async database session
        period_stats: Dictionary mapping agent IDs to their statistics
        period_start: The start time of the period

    """
    logger.debug("Inserting agent periodic stats for %s agents", len(period_stats))

    for agent_id, times in period_stats.items():
        entry = StatAgentPeriodic(
            time=period_start,
            login_time=times.get("login_time", "00:00:00"),
            pause_time=times.get("pause_time", "00:00:00"),
            wrapup_time=times.get("wrapup_time", "00:00:00"),
            stat_agent_id=agent_id,
        )

        session.add(entry)

    await session.flush()


@async_daosession
async def clean_table(session: AsyncSession) -> None:
    """Remove all entries from the StatAgentPeriodic table asynchronously.

    Args:
        session: The async database session

    """
    logger.warning("Cleaning all data from stat_agent_periodic table")
    await session.execute(delete(StatAgentPeriodic))
    await session.flush()


@async_daosession
async def remove_after(session: AsyncSession, date: datetime) -> None:
    """Remove all entries after a specific date asynchronously.

    Args:
        session: The async database session
        date: The date after which to remove entries

    """
    logger.info("Removing agent periodic stats after %s", date)
    await session.execute(
        delete(StatAgentPeriodic).where(StatAgentPeriodic.time >= date)
    )
    await session.flush()
