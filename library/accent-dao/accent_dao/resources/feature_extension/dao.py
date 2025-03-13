# file: accent_dao/resources/feature_extension/dao.py
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.feature_extension import FeatureExtension
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.utils.search import SearchResult

from .database import (
    AgentActionFeatureExtension,
    ForwardFeatureExtension,
    ServiceFeatureExtension,
)
from .persistor import FeatureExtensionPersistor

logger = logging.getLogger(__name__)


@async_daosession
async def async_get_by(session: AsyncSession, **criteria: dict) -> FeatureExtension:
    """Get a feature extension by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The feature extension.

    """
    return await FeatureExtensionPersistor(session).get_by(criteria)


@async_daosession
async def async_find_by(
    session: AsyncSession, **criteria: dict
) -> FeatureExtension | None:
    """Find a feature extension by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The feature extension or None if not found.

    """
    return await FeatureExtensionPersistor(session).find_by(criteria)


@async_daosession
async def async_find_all_by(
    session: AsyncSession, **criteria: dict
) -> list[FeatureExtension]:
    """Find all feature extensions by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of feature extensions.

    """
    return await FeatureExtensionPersistor(session).find_all_by(criteria)


@async_daosession
async def async_get(session: AsyncSession, uuid: str) -> FeatureExtension:
    """Get a feature extension by UUID.

    Args:
        session: The database session.
        uuid: The UUID of the feature extension.

    Returns:
        The feature extension.

    """
    return await FeatureExtensionPersistor(session).get_by({"uuid": uuid})


@async_daosession
async def async_find(session: AsyncSession, uuid: str) -> FeatureExtension | None:
    """Find a feature extension by UUID.

    Args:
        session: The database session.
        uuid: The UUID of the feature extension.

    Returns:
        The feature extension or None if not found.

    """
    return await FeatureExtensionPersistor(session).find_by({"uuid": uuid})


@async_daosession
async def async_search(session: AsyncSession, **parameters: dict) -> SearchResult:
    """Search for feature extensions.

    Args:
        session: The database session.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of items.

    """
    return await FeatureExtensionPersistor(session).search(parameters)


@async_daosession
async def async_create(
    session: AsyncSession, extension: FeatureExtension
) -> FeatureExtension:
    """Create a new feature extension.

    Args:
        session: The database session.
        extension: The feature extension to create.

    Returns:
        The created feature extension.

    """
    return await FeatureExtensionPersistor(session).create(extension)


@async_daosession
async def async_edit(session: AsyncSession, extension: FeatureExtension) -> None:
    """Edit an existing feature extension.

    Args:
        session: The database session.
        extension: The feature extension to edit.

    """
    await FeatureExtensionPersistor(session).edit(extension)


@async_daosession
async def async_delete(session: AsyncSession, extension: FeatureExtension) -> None:
    """Delete a feature extension.

    Args:
        session: The database session.
        extension: The feature extension to delete.

    """
    await FeatureExtensionPersistor(session).delete(extension)


@async_daosession
async def async_find_all_service_extensions(
    session: AsyncSession,
) -> list[ServiceFeatureExtension]:
    """Find all service feature extensions.

    Args:
        session: The database session.

    Returns:
        A list of ServiceFeatureExtension objects.

    """
    return await FeatureExtensionPersistor(session).find_all_service_extensions()


@async_daosession
async def async_find_all_forward_extensions(
    session: AsyncSession,
) -> list[ForwardFeatureExtension]:
    """Find all forward feature extensions.

    Args:
        session: The database session.

    Returns:
        A list of ForwardFeatureExtension objects.

    """
    return await FeatureExtensionPersistor(session).find_all_forward_extensions()


@async_daosession
async def async_find_all_agent_action_extensions(
    session: AsyncSession,
) -> list[AgentActionFeatureExtension]:
    """Find all agent action feature extensions.

    Args:
        session: The database session.

    Returns:
        A list of AgentActionFeatureExtension objects.

    """
    return await FeatureExtensionPersistor(session).find_all_agent_action_extensions()
