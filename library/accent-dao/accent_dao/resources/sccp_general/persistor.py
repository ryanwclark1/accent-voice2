# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.sccpgeneralsettings import SCCPGeneralSettings
from accent_dao.helpers.persistor import AsyncBasePersistor

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class SCCPGeneralSettingsPersistor(AsyncBasePersistor[SCCPGeneralSettings]):
    """Persistor class for SCCPGeneralSettings model."""

    _search_table = SCCPGeneralSettings

    def __init__(self, session: AsyncSession) -> None:
        """Initialize SCCPGeneralSettingsPersistor.

        Args:
            session: Async database session.

        """
        super().__init__(session, self._search_table)

    async def find_all(self) -> list[SCCPGeneralSettings]:
        """Retrieve all SCCP general settings.

        Returns:
            A list of SCCPGeneralSettings objects.

        """
        stmt = select(SCCPGeneralSettings)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def edit_all(
        self, sccp_general_settings: Sequence[SCCPGeneralSettings]
    ) -> None:
        """Edit all SCCP general settings. Replaces existing settings.

        Args:
            sccp_general_settings: A sequence of SCCPGeneralSettings objects.

        """
        # Delete existing settings
        await self.session.execute(delete(SCCPGeneralSettings))

        # Add new settings
        self.session.add_all(sccp_general_settings)
        await self.session.flush()

        logger.info("Updated all SCCP general settings")
