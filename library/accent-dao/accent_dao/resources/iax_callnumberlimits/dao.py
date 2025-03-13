# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.iaxcallnumberlimits import IAXCallNumberLimits
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.iax_callnumberlimits.persistor import (
    IAXCallNumberLimitsPersistor,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


@async_daosession
async def find_all(session: AsyncSession) -> list[IAXCallNumberLimits]:
    """Retrieve all IAX call number limits.

    Args:
        session: The database session.

    Returns:
        A list of IAXCallNumberLimits objects.

    """
    persistor = IAXCallNumberLimitsPersistor(session)
    return await persistor.find_all()


@async_daosession
async def edit_all(
    session: AsyncSession, iax_callnumberlimits: Sequence[IAXCallNumberLimits]
) -> None:
    """Edit all IAX call number limits.

    This will replace the existing IAX call number limits with the provided ones.

    Args:
        session: The database session.
        iax_callnumberlimits: A sequence of IAXCallNumberLimits objects to update.

    """
    persistor = IAXCallNumberLimitsPersistor(session)
    await persistor.edit_all(iax_callnumberlimits)
