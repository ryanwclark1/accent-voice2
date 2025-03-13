# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.iaxcallnumberlimits import IAXCallNumberLimits
from accent_dao.helpers.persistor import AsyncBasePersistor

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class IAXCallNumberLimitsPersistor(AsyncBasePersistor[IAXCallNumberLimits]):
    """Persistor class for IAXCallNumberLimits model."""

    _search_table = IAXCallNumberLimits

    def __init__(self, session: AsyncSession) -> None:
        """Initialize IAXCallNumberLimitsPersistor.

        Args:
            session: Async database session.

        """
        super().__init__(session, self._search_table)

    async def find_all(self) -> list[IAXCallNumberLimits]:
        """Retrieve all IAX call number limits.

        Returns:
            A list of IAXCallNumberLimits objects.

        """
        stmt = select(IAXCallNumberLimits)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def edit_all(
        self, iax_callnumberlimits: Sequence[IAXCallNumberLimits]
    ) -> None:
        """Edit all IAX call number limits.

        This will replace the existing IAX call number limits with the provided ones.

        Args:
            iax_callnumberlimits: A sequence of IAXCallNumberLimits objects to update.

        """
        # Delete existing entries
        await self.session.execute(delete(IAXCallNumberLimits))
        # Add all IAX call number limits
        self.session.add_all(iax_callnumberlimits)
        await self.session.flush()
        logger.info("Updated all IAX call number limits")
