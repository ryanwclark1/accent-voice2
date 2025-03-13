# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.line_extension.persistor import LineExtensionPersistor

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


@async_daosession
async def get_by(session: AsyncSession, **criteria: dict) -> LineExtension:
    """Get a line extension by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The line extension object.

    """
    return await LineExtensionPersistor(session).get_by(criteria)


@async_daosession
async def find_by(session: AsyncSession, **criteria: dict) -> LineExtension | None:
    """Find a line extension by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        The line extension object or None if not found.

    """
    return await LineExtensionPersistor(session).find_by(criteria)


@async_daosession
async def find_all_by(session: AsyncSession, **criteria: dict) -> list[LineExtension]:
    """Find all line extensions by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of line extension objects.

    """
    result: Sequence[LineExtension] = await LineExtensionPersistor(session).find_all_by(
        criteria
    )
    return list(result)


@async_daosession
async def find_all_by_line_id(
    session: AsyncSession, line_id: int
) -> list[LineExtension]:
    """Find all line extensions for a given line ID.

    Args:
        session: The database session.
        line_id: The ID of the line.

    Returns:
        A list of line extension objects.
    """
    return await LineExtensionPersistor(session).find_all_by(line_id=line_id)


@async_daosession
async def find_by_line_id(session: AsyncSession, line_id: int) -> LineExtension | None:
    """Find a line extension by line ID.

    Args:
        session: The database session.
        line_id: The ID of the line.

    Returns:
        The line extension object or None if not found.

    """
    return await LineExtensionPersistor(session).find_by(line_id=line_id)


@async_daosession
async def find_by_extension_id(
    session: AsyncSession, extension_id: int
) -> LineExtension | None:
    """Find a line extension by extension ID.

    Args:
        session: The database session.
        extension_id: The ID of the extension.

    Returns:
        The line extension object or None if not found.

    """
    return await LineExtensionPersistor(session).find_by(extension_id=extension_id)


@async_daosession
async def associate(
    session: AsyncSession, line: LineFeatures, extension: Extension
) -> LineExtension:
    """Associate a line with an extension.

    Args:
        session: The database session.
        line: The line object.
        extension: The extension object.

    Returns:
        The created or existing LineExtension object.

    """
    return await LineExtensionPersistor(session).associate_line_extension(
        line, extension
    )


@async_daosession
async def dissociate(
    session: AsyncSession, line: LineFeatures, extension: Extension
) -> None:
    """Dissociate a line from an extension.

    Args:
        session: The database session.
        line: The line object.
        extension: The extension object.

    """
    await LineExtensionPersistor(session).dissociate_line_extension(line, extension)
