# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.queueskillrule import QueueSkillRule
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class SkillRulePersistor(CriteriaBuilderMixin, AsyncBasePersistor[QueueSkillRule]):
    """Persistor class for QueueSkillRule model."""

    _search_table = QueueSkillRule

    def __init__(
        self,
        session: AsyncSession,
        skill_rule_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize SkillRulePersistor.

        Args:
            session: Async database session.
            skill_rule_search: Search system for skill rules.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = skill_rule_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find skill rules based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(QueueSkillRule)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching skill rules."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> QueueSkillRule:
        """Retrieve a single skill rule by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            QueueSkillRule: The found skill rule.

        Raises:
            NotFoundError: If no skill rule is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("SkillRule", **criteria)
        return model

    async def find_all_by(self, criteria: dict[str, Any]) -> list[QueueSkillRule]:
        """Find all QueueSkillRule by criteria.

        Returns:
            list of QueueSkillRule.

        """
        result: Sequence[QueueSkillRule] = await super().find_all_by(criteria)
        return list(result)
