# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.staticiax import StaticIAX
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.iax_general.persistor import IAXGeneralPersistor

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


@async_daosession
async def find_all(session: AsyncSession) -> list[StaticIAX]:
    """Retrieve all IAX general settings.

    Args:
        session: The database session.

    Returns:
        A list of StaticIAX objects representing the settings.

    """
    persistor = IAXGeneralPersistor(session)
    return await persistor.find_all()


@async_daosession
async def edit_all(session: AsyncSession, iax_general: Sequence[StaticIAX]) -> None:
    """Edit all IAX general settings.

    This will replace the existing IAX general settings with the provided ones.

    Args:
        session: The database session.
        iax_general: A sequence of StaticIAX objects representing the new settings.

    """
    persistor = IAXGeneralPersistor(session)
    await persistor.edit_all(iax_general)
