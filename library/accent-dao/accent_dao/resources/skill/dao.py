# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.queueskill import QueueSkill
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.skill.persistor import SkillPersistor
from accent_dao.resources.skill.search import skill_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for skills.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of skills.

    """
    return await SkillPersistor(session, skill_search, tenant_uuids).search(parameters)


@async_daosession
async def get(
    session: AsyncSession, skill_id: int, tenant_uuids: list[str] | None = None
) -> QueueSkill:
    """Get a skill by ID.

    Args:
        session: The database session.
        skill_id: The ID of the skill.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The skill object.

    """
    return await SkillPersistor(session, skill_search, tenant_uuids).get_by(
        {"id": skill_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> QueueSkill:
    """Get a skill by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The skill object.

    """
    return await SkillPersistor(session, skill_search, tenant_uuids).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession, skill_id: int, tenant_uuids: list[str] | None = None
) -> QueueSkill | None:
    """Find a skill by ID.

    Args:
        session: The database session.
        skill_id: The ID of the skill.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The skill object or None if not found.

    """
    return await SkillPersistor(session, skill_search, tenant_uuids).find_by(
        {"id": skill_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> QueueSkill | None:
    """Find a skill by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The skill object or None if not found.

    """
    return await SkillPersistor(session, skill_search, tenant_uuids).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[QueueSkill]:
    """Find all skills by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of skill objects.

    """
    result: Sequence[QueueSkill] = await SkillPersistor(
        session, skill_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, skill: QueueSkill) -> QueueSkill:
    """Create a new skill.

    Args:
        session: The database session.
        skill: The skill object to create.

    Returns:
        The created skill object.

    """
    return await SkillPersistor(session, skill_search).create(skill)


@async_daosession
async def edit(session: AsyncSession, skill: QueueSkill) -> None:
    """Edit an existing skill.

    Args:
        session: The database session.
        skill: The skill object to edit.

    """
    await SkillPersistor(session, skill_search).edit(skill)


@async_daosession
async def delete(session: AsyncSession, skill: QueueSkill) -> None:
    """Delete a skill.

    Args:
        session: The database session.
        skill: The skill object to delete.

    """
    await SkillPersistor(session, skill_search).delete(skill)
