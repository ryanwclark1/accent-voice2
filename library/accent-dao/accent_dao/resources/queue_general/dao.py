# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.staticqueue import StaticQueue
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.queue_general.persistor import QueueGeneralPersistor

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


@async_daosession
async def find_all(session: AsyncSession) -> list[StaticQueue]:
    """Retrieve all static queue general settings.

    Args:
        session: The database session.

    Returns:
        A list of StaticQueue objects representing the settings.

    """
    persistor = QueueGeneralPersistor(session)
    return await persistor.find_all()


@async_daosession
async def edit_all(session: AsyncSession, queue_general: Sequence[StaticQueue]) -> None:
    """Edit all static queue general settings.

    This will replace the existing settings with the provided ones.

    Args:
        session: The database session.
        queue_general: A sequence of StaticQueue objects representing the new settings.

    """
    persistor = QueueGeneralPersistor(session)
    await persistor.edit_all(queue_general)
