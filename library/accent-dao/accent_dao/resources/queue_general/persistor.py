# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy import and_, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.staticqueue import StaticQueue
from accent_dao.helpers.persistor import AsyncBasePersistor

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class QueueGeneralPersistor(AsyncBasePersistor[StaticQueue]):
    """Persistor class for Queue general settings (StaticQueue model)."""

    _search_table = StaticQueue

    def __init__(self, session: AsyncSession) -> None:
        """Initialize QueueGeneralPersistor.

        Args:
            session: Async database session.
        """
        super().__init__(session, self._search_table)

    async def find_all(self) -> list[StaticQueue]:
        """Retrieve all static queue general settings.

        Returns:
            A list of StaticQueue objects.

        """
        stmt = (
            select(StaticQueue)
            .filter(
                and_(
                    StaticQueue.category == "general", StaticQueue.var_val.is_not(None)
                )
            )
            .order_by(StaticQueue.var_metric.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def edit_all(self, queue_general: Sequence[StaticQueue]) -> None:
        """Edit all static queue general settings. Replaces existing with provided.

        Args:
            queue_general: A sequence of StaticQueue objects.

        """
        # Delete existing general settings.
        await self.session.execute(
            delete(StaticQueue).where(StaticQueue.category == "general")
        )

        # Add all new settings
        for setting in queue_general:
            setting.filename = "queues.conf"
            setting.category = "general"
            setting.id = None  # Ensure new rows for SQLA 2.0+
        self.session.add_all(queue_general)
        await self.session.flush()

        logger.info("Updated all queue general settings")
