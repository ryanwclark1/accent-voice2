# file: accent_dao/resources/access_feature/dao.py
# Copyright 2025 Accent Communications

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.accessfeatures import AccessFeatures
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .persistor import AccessFeaturesPersistor
from .search import access_feature_search


@async_daosession
async def search(session: AsyncSession, **parameters: dict) -> SearchResult:
    """Search for access features.

    Args:
        session: The database session.
        **parameters: Keyword arguments for search parameters.

    Returns:
        SearchResult: The search results.

    """
    return await AccessFeaturesPersistor(session, access_feature_search).search(
        parameters
    )


@async_daosession
async def get(session: AsyncSession, access_feature_id: int) -> AccessFeatures:
    """Get an access feature by ID.

    Args:
        session: The database session.
        access_feature_id: The ID of the access feature.

    Returns:
        AccessFeatures: The access feature.

    """
    return await AccessFeaturesPersistor(session, access_feature_search).get_by(
        {"id": access_feature_id}
    )


@async_daosession
async def get_by(session: AsyncSession, **criteria: dict) -> AccessFeatures:
    """Get an access feature by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        AccessFeatures: The access feature.

    """
    return await AccessFeaturesPersistor(session, access_feature_search).get_by(
        criteria
    )


@async_daosession
async def find(session: AsyncSession, access_feature_id: int) -> AccessFeatures | None:
    """Find an access feature by ID.

    Args:
        session: The database session.
        access_feature_id: The ID of the access feature.

    Returns:
        AccessFeatures | None: The access feature, or None if not found.

    """
    return await AccessFeaturesPersistor(session, access_feature_search).find_by(
        {"id": access_feature_id}
    )


@async_daosession
async def find_by(session: AsyncSession, **criteria: dict) -> AccessFeatures | None:
    """Find an access feature by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        AccessFeatures | None: The access feature, or None if not found.

    """
    return await AccessFeaturesPersistor(session, access_feature_search).find_by(
        criteria
    )


@async_daosession
async def find_all_by(session: AsyncSession, **criteria: dict) -> list[AccessFeatures]:
    """Find all access features by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        list[AccessFeatures]: A list of access features.

    """
    return await AccessFeaturesPersistor(session, access_feature_search).find_all_by(
        criteria
    )


@async_daosession
async def create(
    session: AsyncSession, access_feature: AccessFeatures
) -> AccessFeatures:
    """Create a new access feature.

    Args:
        session: The database session.
        access_feature: The access feature to create.

    Returns:
        AccessFeatures: The created access feature.

    """
    return await AccessFeaturesPersistor(session, access_feature_search).create(
        access_feature
    )


@async_daosession
async def edit(session: AsyncSession, access_feature: AccessFeatures) -> None:
    """Edit an existing access feature.

    Args:
        session: The database session.
        access_feature: The access feature to edit.

    """
    await AccessFeaturesPersistor(session, access_feature_search).edit(access_feature)


@async_daosession
async def delete(session: AsyncSession, access_feature: AccessFeatures) -> None:
    """Delete an access feature.

    Args:
        session: The database session.
        access_feature: The access feature to delete.

    """
    await AccessFeaturesPersistor(session, access_feature_search).delete(access_feature)
