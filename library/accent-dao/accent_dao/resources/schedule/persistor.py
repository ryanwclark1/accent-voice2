# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.schedule import Schedule
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class SchedulePersistor(CriteriaBuilderMixin, AsyncBasePersistor[Schedule]):
    """Persistor class for Schedule model."""

    _search_table = Schedule

    def __init__(
        self,
        session: AsyncSession,
        schedule_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize SchedulePersistor.

        Args:
            session: Async database session.
            schedule_search: Search system for schedules.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = schedule_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find schedules based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Schedule)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching schedules."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> Schedule:
        """Retrieve a single schedule by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Schedule: The found schedule.

        Raises:
            NotFoundError: If no schedule is found.

        """
        schedule = await self.find_by(criteria)
        if not schedule:
            raise errors.NotFoundError("Schedule", **criteria)
        return schedule

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Schedule]:
        """Find all Schedule by criteria.

        Returns:
            list of Schedule.

        """
        result: Sequence[Schedule] = await super().find_all_by(criteria)
        return list(result)
