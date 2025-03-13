# file: accent_dao/resources/meeting/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.meeting import Meeting, MeetingOwner
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class MeetingPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Meeting]):
    """Persistor class for Meeting model."""

    _search_table = Meeting

    def __init__(
        self,
        session: AsyncSession,
        search_system: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize MeetingPersistor.

        Args:
            session: Async database session.
            search_system: Search system for meetings.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = search_system
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find meetings based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Meeting)
        query = self._filter_tenant_uuid(query)
        query = self._filter_owner(query, criteria)
        query = self._filter_created_before(query, criteria)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching meetings.

        Returns:
            SQLAlchemy query object.

        """
        return select(self.search_system.config.table)

    def _filter_tenant_uuid(self, query: Any) -> Any:
        """Filter query by tenant UUID.

        Args:
            query: The query object.

        Returns:
            The filtered query object.

        """
        if self.tenant_uuids is not None:
            query = query.filter(Meeting.tenant_uuid.in_(self.tenant_uuids))
        return query

    def _filter_owner(self, query: Any, criteria: dict[str, Any]) -> Any:
        """Filter by owner."""
        owner = criteria.pop("owner", None)
        if not owner:
            return query

        owner_meeting = self.session.query(MeetingOwner.meeting_uuid).filter(
            MeetingOwner.user_uuid == owner
        )
        query = query.filter(Meeting.uuid.in_(owner_meeting))

        return query

    def _filter_created_before(self, query: Any, criteria: dict[str, Any]) -> Any:
        """Filter by created_before."""
        before = criteria.pop("created_before", None)
        if not before:
            return query

        return query.filter(Meeting.created_at < before)

    async def get_by(self, criteria: dict[str, Any]) -> Meeting:
        """Retrieve a single meeting by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Meeting: The found meeting.

        Raises:
            NotFoundError: If no meeting is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("Meeting", **criteria)
        return model

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for meetings.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = await self._search_query()
        query = self._filter_tenant_uuid(query)
        query = self._filter_owner(query, parameters)
        query = self._filter_created_before(query, parameters)
        rows, total = await self.search_system.async_search_from_query(
            self.session, query, parameters
        )
        return SearchResult(total, rows)

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Meeting]:
        """Find all Meeting by criteria.

        Returns:
            list of Meeting.

        """
        result: Sequence[Meeting] = await super().find_all_by(criteria)
        return list(result)
