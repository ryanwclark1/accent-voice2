# file: accent_dao/resources/voicemail_zonemessages/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.staticvoicemail import StaticVoicemail
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.voicemail_zonemessages.persistor import (
    VoicemailZoneMessagesPersistor,
)

logger = logging.getLogger(__name__)


@async_daosession
async def find_all(session: AsyncSession) -> list[StaticVoicemail]:
    """Find all voicemail zonemessage settings.

    Args:
        session: The database session.

    Returns:
        A list of StaticVoicemail objects representing the zonemessage settings.

    """
    query = (
        select(StaticVoicemail)
        .filter(StaticVoicemail.category == "zonemessages")
        .filter(StaticVoicemail.var_val.is_not(None))
    )
    result = await session.execute(query)
    return result.scalars().all()


@async_daosession
async def edit_all(
    session: AsyncSession, voicemail_zonemessages: list[StaticVoicemail]
) -> None:
    """Edit all voicemail zonemessage settings.

    Args:
        session: The database session.
        voicemail_zonemessages: A list of StaticVoicemail objects with updated values.

    """
    await VoicemailZoneMessagesPersistor(session).edit_all(voicemail_zonemessages)
