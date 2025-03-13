# file: accent_dao/resources/conference/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.conference import Conference
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class ConferencePersistor(CriteriaBuilderMixin, AsyncBasePersistor[Conference]):
    """Persistor class for Conference model."""

    _search_table = Conference

    def __init__(
        self,
        session: AsyncSession,
        conference_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize ConferencePersistor.

        Args:
            session: Async database session.
            conference_search: Search system for conferences.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = conference_search
        self.tenant_uuids = tenant_uuids
        self.session = session  # Keep this for now

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find conferences based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Conference)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> Conference:
        """Retrieve a single conference by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Conference: The found conference.

        Raises:
            NotFoundError: If no conference is found.

        """
        model = await self.find_by(criteria)
        if not model:
            msg = "Conference"
            raise errors.NotFoundError(msg, **criteria)
        return model

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for conferences.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = await self._search_query()
        query = self._filter_tenant_uuid(query)
        rows, total = await self.search_system.search_from_query(
            self.session, query, parameters
        )
        return SearchResult(total, rows)

    async def _search_query(self) -> Any:
        """Build the base search query."""
        return select(self.search_system.config.table)

    def _filter_tenant_uuid(self, query: Any) -> Any:
        """Filter query by tenant UUID."""
        if self.tenant_uuids is not None:
            query = query.filter(Conference.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Conference]:
        """Find all by criteria.

        Args:
            criteria (dict): Filtering criteria.

        Returns:
             list: List of all matching Conference instances.

        """
        result: Sequence[Conference] = await super().find_all_by(criteria)
        return list(result)
