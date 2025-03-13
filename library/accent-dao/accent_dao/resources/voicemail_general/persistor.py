# file: accent_dao/resources/voicemail_general/persistor.py
# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.staticvoicemail import StaticVoicemail
from accent_dao.helpers.persistor import AsyncBasePersistor

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class VoicemailGeneralPersistor(AsyncBasePersistor[StaticVoicemail]):
    """Persistor class for StaticVoicemail model (general settings)."""

    _search_table = StaticVoicemail

    def __init__(self, session: AsyncSession) -> None:
        """Initialize VoicemailGeneralPersistor.

        Args:
            session: Async database session.

        """
        super().__init__(session, self._search_table)
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
            setting.cat_metric = 1
            setting.id = None  # Remove any existing ID to avoid conflicts and let auto increment work
            self.session.add(setting)  # Use add instead of merge
        await self.session.flush()
