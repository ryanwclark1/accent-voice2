# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.paging import Paging
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class PagingPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Paging]):
    """Persistor class for Paging model."""

    _search_table = Paging

    def __init__(
        self,
        session: AsyncSession,
        paging_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize PagingPersistor.

        Args:
            session: Async database session.
            paging_search: Search system for paging groups.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = paging_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find paging groups based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Paging)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching paging groups."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> Paging:
        """Retrieve a single paging group by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Paging: The found paging group.

        Raises:
            NotFoundError: If no paging group is found.

        """
        paging = await self.find_by(criteria)
        if not paging:
            raise errors.NotFoundError("Paging", **criteria)
        return paging

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Paging]:
        """Find all Paging by criteria.

        Returns:
            list of Paging.

        """
        result: Sequence[Paging] = await super().find_all_by(criteria)
        return list(result)
