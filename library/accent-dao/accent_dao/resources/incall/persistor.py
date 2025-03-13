# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.incall import Incall
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from accent_dao.alchemy.dialaction import Dialaction
    from collections.abc import Sequence


class IncallPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Incall]):
    """Persistor class for Incall model."""

    _search_table = Incall

    def __init__(
        self,
        session: AsyncSession,
        incall_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize IncallPersistor.

        Args:
            session: Async database session.
            incall_search: Search system for incalls.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = incall_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find incalls based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Incall)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching incalls."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> Incall:
        """Retrieve a single incall by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Incall: The found incall.

        Raises:
            NotFoundError: If no incall is found.

        """
        incall = await self.find_by(criteria)
        if not incall:
            raise errors.NotFoundError("Incall", **criteria)
        return incall

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for incalls.

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

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Incall]:
        """Find all InCall by criteria.

        Returns:
            list of InCall.

        """
        result: Sequence[Incall] = await super().find_all_by(criteria)
        return list(result)

    async def create(self, incall: Incall) -> Incall:
        """Create a new incall record.

        If no destination is provided, set a default 'none' action.

        Args:
            incall: The incall object to create.

        Returns:
            The created incall object.

        """
        if not incall.destination:
            incall.destination = Dialaction(action="none")

        return await super().create(incall)

    async def update_destination(
        self, incall: Incall, destination: "Dialaction"
    ) -> None:
        """Update the destination of an incall route.

        Args:
            incall: The incall route object.
            destination: The new destination dialaction.

        """
        incall.destination = destination
        await self.session.flush()
