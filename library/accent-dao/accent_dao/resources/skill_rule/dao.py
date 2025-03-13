# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.queueskillrule import QueueSkillRule
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.skill_rule.persistor import SkillRulePersistor
from accent_dao.resources.skill_rule.search import skill_rule_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for skill rules.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of skill rules.

    """
    return await SkillRulePersistor(session, skill_rule_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def get(
    session: AsyncSession, skill_rule_id: int, tenant_uuids: list[str] | None = None
) -> QueueSkillRule:
    """Get a skill rule by ID.

    Args:
        session: The database session.
        skill_rule_id: The ID of the skill rule.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The skill rule object.

    """
    return await SkillRulePersistor(session, skill_rule_search, tenant_uuids).get_by(
        {"id": skill_rule_id}
    )


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> QueueSkillRule:
    """Get a skill rule by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The skill rule object.

    """
    return await SkillRulePersistor(session, skill_rule_search, tenant_uuids).get_by(
        criteria
    )


@async_daosession
async def find(
    session: AsyncSession, skill_rule_id: int, tenant_uuids: list[str] | None = None
) -> QueueSkillRule | None:
    """Find a skill rule by ID.

    Args:
        session: The database session.
        skill_rule_id: The ID of the skill rule.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The skill rule object or None if not found.

    """
    return await SkillRulePersistor(session, skill_rule_search, tenant_uuids).find_by(
        {"id": skill_rule_id}
    )


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> QueueSkillRule | None:
    """Find a skill rule by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The skill rule object or None if not found.

    """
    return await SkillRulePersistor(session, skill_rule_search, tenant_uuids).find_by(
        criteria
    )


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[QueueSkillRule]:
    """Find all skill rules by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of skill rule objects.

    """
    result: Sequence[QueueSkillRule] = await SkillRulePersistor(
        session, skill_rule_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, skill_rule: QueueSkillRule) -> QueueSkillRule:
    """Create a new skill rule.

    Args:
        session: The database session.
        skill_rule: The skill rule object to create.

    Returns:
        The created skill rule object.

    """
    return await SkillRulePersistor(session, skill_rule_search).create(skill_rule)


@async_daosession
async def edit(session: AsyncSession, skill_rule: QueueSkillRule) -> None:
    """Edit an existing skill rule.

    Args:
        session: The database session.
        skill_rule: The skill rule object to edit.

    """
    await SkillRulePersistor(session, skill_rule_search).edit(skill_rule)


@async_daosession
async def delete(session: AsyncSession, skill_rule: QueueSkillRule) -> None:
    """Delete a skill rule.

    Args:
        session: The database session.
        skill_rule: The skill rule object to delete.

    """
    await SkillRulePersistor(session, skill_rule_search).delete(skill_rule)
