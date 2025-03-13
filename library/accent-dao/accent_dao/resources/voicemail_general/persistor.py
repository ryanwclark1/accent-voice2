# file: accent_dao/resources/voicemail_general/persistor.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.staticvoicemail import StaticVoicemail

logger = logging.getLogger(__name__)


class VoicemailGeneralPersistor:
    """Persistor class for StaticVoicemail model (general settings)."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize VoicemailGeneralPersistor.

        Args:
            session: Async database session.

        """
        self.session = session

    async def find_all(self) -> list[StaticVoicemail]:
        """Find all static voicemail general settings.

        Returns:
            A list of StaticVoicemail objects.

        """
        query = (
            select(StaticVoicemail)
            .filter(StaticVoicemail.category == "general")
            .filter(StaticVoicemail.var_val.is_not(None))
            .order_by(StaticVoicemail.var_metric.asc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def edit_all(self, voicemail_general: list[StaticVoicemail]) -> None:
        """Edit all static voicemail general settings.

        Args:
            voicemail_general: The list of StaticVoicemail objects with updated values.

        """
        # Delete existing general settings
        await self.session.execute(
            delete(StaticVoicemail).where(StaticVoicemail.category == "general")
        )

        # Prepare and add new settings
        for setting in voicemail_general:
            setting.filename = "voicemail.conf"
            setting.category = "general"
            # Avoid autoincrement issues.  Don't set the PK.
            setting.id = None  # Assuming id is the primary key and auto-incrementing
            self.session.add(setting)

        await self.session.flush()
