# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.moh import MOH
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class MOHPersistor(CriteriaBuilderMixin, AsyncBasePersistor[MOH]):
    """Persistor class for MOH model."""

    _search_table = MOH

    def __init__(
        self,
        session: AsyncSession,
        moh_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize MOHPersistor.

        Args:
            session: Async database session.
            moh_search: Search system for MOH.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = moh_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find MOH entries based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(MOH)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching MOH entries."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> MOH:
        """Retrieve a single MOH entry by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            MOH: The found MOH entry.

        Raises:
            NotFoundError: If no MOH entry is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("MOH", **criteria)
        return model

    async def find_all_by(self, criteria: dict[str, Any]) -> list[MOH]:
        """Find all MOH by criteria.

        Returns:
            list of MOH.

        """
        result: Sequence[MOH] = await super().find_all_by(criteria)
        return list(result)
