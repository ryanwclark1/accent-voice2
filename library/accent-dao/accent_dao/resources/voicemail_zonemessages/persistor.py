# file: accent_dao/resources/voicemail_zonemessages/persistor.py
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


class VoicemailZoneMessagesPersistor(AsyncBasePersistor[StaticVoicemail]):
    """Persistor class for StaticVoicemail model (zonemessages settings)."""

    _search_table = StaticVoicemail

    def __init__(self, session: AsyncSession) -> None:
        """Initialize VoicemailZoneMessagesPersistor.

        Args:
            session: Async database session.

        """
        super().__init__(session, self._search_table)
        self.session = session

    async def find_all(self) -> list[StaticVoicemail]:
        """Find all static voicemail zonemessages settings.

        Returns:
            A list of StaticVoicemail objects.

        """
        query = (
            select(StaticVoicemail)
            .filter(StaticVoicemail.category == "zonemessages")
            .filter(StaticVoicemail.var_val.is_not(None))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def edit_all(self, voicemail_zonemessages: list[StaticVoicemail]) -> None:
        """Edit all static voicemail zonemessages settings.

        Args:
            voicemail_zonemessages: The list of StaticVoicemail objects with updated values.

        """
        # Delete existing zonemessages settings
        await self.session.execute(
            delete(StaticVoicemail).where(StaticVoicemail.category == "zonemessages")
        )

        # Prepare and add new settings
        for setting in voicemail_zonemessages:
            setting.filename = "voicemail.conf"
            setting.category = "zonemessages"
            setting.cat_metric = 1  # Explicitly set to 1
            setting.id = None  # Remove any existing ID to avoid conflicts. let the auto increment work
            self.session.add(setting)

        await self.session.flush()
