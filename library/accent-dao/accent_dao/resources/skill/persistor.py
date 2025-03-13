# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.queueskill import QueueSkill
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class SkillPersistor(CriteriaBuilderMixin, AsyncBasePersistor[QueueSkill]):
    """Persistor class for QueueSkill model."""

    _search_table = QueueSkill

    def __init__(
        self,
        session: AsyncSession,
        skill_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize SkillPersistor.

        Args:
            session: Async database session.
            skill_search: Search system for skills.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = skill_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find skills based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(QueueSkill)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching skills."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> QueueSkill:
        """Retrieve a single skill by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            QueueSkill: The found skill.

        Raises:
            NotFoundError: If no skill is found.

        """
        skill = await self.find_by(criteria)
        if not skill:
            raise errors.NotFoundError("Skill", **criteria)
        return skill

    async def find_all_by(self, criteria: dict[str, Any]) -> list[QueueSkill]:
        """Find all QueueSkill by criteria.

        Returns:
            list of QueueSkill.

        """
        result: Sequence[QueueSkill] = await super().find_all_by(criteria)
        return list(result)
