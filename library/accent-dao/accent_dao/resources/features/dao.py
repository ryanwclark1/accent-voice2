# file: accent_dao/resources/features/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.features import Features
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.helpers.exception import NotFoundError

from .persistor import FeaturesPersistor

logger = logging.getLogger(__name__)


@async_daosession
async def find_all(session: AsyncSession, section: str) -> list[Features]:
    """Find all features for a given section.

    Args:
        session: The database session.
        section: The section to filter features by.

    Returns:
        A list of Feature objects.

    """
    return await FeaturesPersistor(session).find_all(section)


@async_daosession
async def edit_all(
    session: AsyncSession, section: str, features: list[Features]
) -> None:
    """Edit all features for a given section.

    Args:
        session: The database session.
        section: The section to update features in.
        features: The list of Feature objects with updated values.

    """
    await FeaturesPersistor(session).edit_all(section, features)


@async_daosession
async def get_value(session: AsyncSession, feature_id: int) -> str | None:
    """Get the value of a specific feature by its ID.

    Args:
        session: The database session.
        feature_id: The ID of the feature.

    Returns:
        The value of the feature, or None if not found.

    Raises:
        NotFoundError: If no feature is found with the given ID.

    """
    result = await session.execute(
        select(Features.var_val).where(Features.id == feature_id)
    )
    value = result.scalar_one_or_none()

    if not value:
        raise NotFoundError("Features", id=feature_id)

    value = value.split(",", 1)[0]
    return value
