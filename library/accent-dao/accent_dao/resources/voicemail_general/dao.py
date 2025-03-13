# file: accent_dao/resources/voicemail_general/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.staticvoicemail import StaticVoicemail
from accent_dao.helpers.db_manager import async_daosession

logger = logging.getLogger(__name__)


@async_daosession
async def async_find_all(session: AsyncSession) -> list[StaticVoicemail]:
    """Find all static voicemail general settings.

    Args:
        session: The database session.

    Returns:
        A list of StaticVoicemail objects.

    """
    # Use select for SQLAlchemy 2.x style
    query = (
        select(StaticVoicemail)
        .filter(StaticVoicemail.category == "general")
        .filter(StaticVoicemail.var_val.is_not(None))
        .order_by(StaticVoicemail.var_metric.asc())
    )
    result = await session.execute(query)
    return result.scalars().all()


@async_daosession
async def async_edit_all(
    session: AsyncSession, voicemail_general: list[StaticVoicemail]
) -> None:
    """Edit all static voicemail general settings.

    Args:
        session: The database session.
        voicemail_general:  The list of StaticVoicemail objects with updated values.

    """
    # Efficient deletion of existing general settings
    await session.execute(
        delete(StaticVoicemail).where(StaticVoicemail.category == "general")
    )

    # Prepare new settings
    for setting in voicemail_general:
        setting.filename = "voicemail.conf"
        setting.category = "general"
        session.add(setting)  # Stage all new settings for addition

    await session.flush()
