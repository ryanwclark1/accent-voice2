# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.sccpgeneralsettings import SCCPGeneralSettings
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.sccp_general.persistor import SCCPGeneralSettingsPersistor

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


@async_daosession
async def find_all(session: AsyncSession) -> list[SCCPGeneralSettings]:
    """Retrieve all SCCP general settings.

    Args:
        session: The database session.

    Returns:
        A list of SCCPGeneralSettings objects.

    """
    persistor = SCCPGeneralSettingsPersistor(session)
    return await persistor.find_all()


@async_daosession
async def edit_all(
    session: AsyncSession, sccp_general_settings: Sequence[SCCPGeneralSettings]
) -> None:
    """Edit all SCCP general settings.

    This replaces the existing settings with the provided ones.

    Args:
        session: The database session.
        sccp_general_settings: A sequence of SCCPGeneralSettings objects.

    """
    persistor = SCCPGeneralSettingsPersistor(session)
    await persistor.edit_all(sccp_general_settings)
