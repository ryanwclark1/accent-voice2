# file: accent_dao/resources/configuration/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.infos import Infos
from accent_dao.helpers.db_manager import async_daosession


@async_daosession
async def async_is_live_reload_enabled(session: AsyncSession) -> bool:
    """Check if live reload is enabled.

    Args:
        session: The database session.

    Returns:
        bool: True if live reload is enabled, False otherwise.

    """
    stmt = select(Infos.live_reload_enabled)
    result = await session.execute(stmt)
    # Use scalar_one_or_none() as there should only be one row
    enabled = result.scalar_one_or_none()

    # Handle the case where no row exists. Return False, same behavior as original.
    if enabled is None:
        return False
    return enabled


@async_daosession
async def async_set_live_reload_status(session: AsyncSession, data: dict) -> None:
    """Set the live reload status.

    Args:
        session: The database session.
        data: Dictionary containing the new status.  Expects 'enabled' key.

    """
    enabled = data["enabled"]
    # Use update for SQLAlchemy 2.x style.  Also, use bindparam for security
    stmt = update(Infos).values(live_reload_enabled=enabled)

    await session.execute(stmt)
    await session.flush()


@async_daosession
async def async_get_config(session: AsyncSession) -> Infos | None:
    """Retrieve all Infos.

    Args:
        session: The database session.

    Returns:
    Infos: Infos or None.

    """
    query = select(Infos)
    result = await session.execute(query)
    return result.scalars().first()


@async_daosession
async def async_set_timezone(session: AsyncSession, timezone: str) -> None:
    """Set the timezone.

    Args:
        session: The database session.
        timezone (str): The timezone string to set, ex: "America/New_York".

    """
    update_stmt = update(Infos).values(timezone=timezone)

    await session.execute(update_stmt)
    await session.flush()


@async_daosession
async def async_get_timezone(session: AsyncSession) -> str | None:
    """Get the timezone.

    Args:
        session: The database session.

    Returns:
    str | None: The timezone string.

    """
    select_stmt = select(Infos.timezone)
    result = await session.execute(select_stmt)
    return result.scalar_one_or_none()


@async_daosession
async def async_set_configured_flag(session: AsyncSession) -> None:
    """Set the configured flag to true.

    Args:
        session: The database session.

    """
    update_stmt = update(Infos).values(configured=True)

    await session.execute(update_stmt)
    await session.flush()


@async_daosession
async def async_get_configured_flag(session: AsyncSession) -> bool:
    """Check if the system is configured.

    Args:
        session: The database session.

    Returns:
      bool: The value of the configured flag.

    """
    stmt = select(Infos.configured)
    result = await session.execute(stmt)
    return result.scalar_one_or_none() or False
