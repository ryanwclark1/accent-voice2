# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.meeting import Meeting
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class MeetingPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Meeting]):
    """Persistor class for Meeting model."""

    _search_table = Meeting

    def __init__(
        self,
        session: AsyncSession,
        meeting_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize MeetingPersistor.

        Args:
            session: Async database session.
            meeting_search: Search system for meetings.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = meeting_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find meetings based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Meeting)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching meetings."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> Meeting:
        """Retrieve a single meeting by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Meeting: The found meeting.

        Raises:
            NotFoundError: If no meeting is found.

        """
        meeting = await self.find_by(criteria)
        if not meeting:
            raise errors.NotFoundError("Meeting", **criteria)
        return meeting

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Meeting]:
        """Find all Meeting by criteria.

        Returns:
            list of Meeting.

        """
        result: Sequence[Meeting] = await super().find_all_by(criteria)
        return list(result)
