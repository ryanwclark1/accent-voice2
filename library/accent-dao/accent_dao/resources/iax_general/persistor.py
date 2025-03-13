# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.staticiax import StaticIAX
from accent_dao.helpers.persistor import AsyncBasePersistor

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class IAXGeneralPersistor(AsyncBasePersistor[StaticIAX]):
    """Persistor class for IAX general settings."""

    _search_table = StaticIAX

    def __init__(self, session: AsyncSession) -> None:
        """Initialize IAXGeneralPersistor.

        Args:
            session: Async database session.

        """
        super().__init__(session, self._search_table)

    async def find_all(self) -> list[StaticIAX]:
        """Retrieve all IAX general settings.

        Returns:
            A list of StaticIAX objects representing the settings.

        """
        stmt = (
            select(StaticIAX)
            .filter(
                and_(
                    StaticIAX.category == "general",
                    StaticIAX.var_name != "register",
                    StaticIAX.var_val.is_not(None),
                )
            )
            .order_by(StaticIAX.var_metric.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def edit_all(self, iax_general: Sequence[StaticIAX]) -> None:
        """Edit all IAX general settings.

        This will replace the existing IAX general settings with the provided ones.

        Args:
            iax_general: A sequence of StaticIAX objects representing the new settings.

        """
        # Delete existing general settings, excluding 'register'
        await self.session.execute(
            delete(StaticIAX).where(
                and_(StaticIAX.category == "general", StaticIAX.var_name != "register")
            )
        )

        # Add all new settings
        for setting in iax_general:
            setting.filename = "iax.conf"
            setting.category = "general"
            setting.id = None  # Ensure new rows for SQLA 2.0+
        self.session.add_all(iax_general)
        await self.session.flush()

        logger.info("Updated all IAX general settings")
