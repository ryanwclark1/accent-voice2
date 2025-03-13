# file: accent_dao/resources/switchboard/persistor.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.switchboard import Switchboard
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class SwitchboardPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Switchboard]):
    """Persistor class for Switchboard model."""

    _search_table = Switchboard

    def __init__(
        self,
        session: AsyncSession,
        search_system: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize SwitchboardPersistor.

        Args:
            session: Async database session.
            search_system: Search system for switchboards.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = search_system
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find switchboards based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Switchboard)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> Switchboard:
        """Retrieve a single switchboard by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Switchboard: The found switchboard.

        Raises:
            NotFoundError: If no switchboard is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("Switchboard", **criteria)
        return model

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for switchboards.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = await self._search_query()
        query = self._filter_tenant_uuid(query)
        rows, total = await self.search_system.async_search_from_query(
            self.session, query, parameters
        )
        return SearchResult(total, rows)

    async def _search_query(self) -> Any:
        """Create a query for searching switchboards.

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
            query = query.filter(Switchboard.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Switchboard]:
        """Find all Switchboard by criteria.

        Returns:
            list of Switchboard.

        """
        result: Sequence[Switchboard] = await super().find_all_by(criteria)
        return list(result)
