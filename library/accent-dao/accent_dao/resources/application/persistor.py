# file: accent_dao/resources/application/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.application import Application
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence


class ApplicationPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Application]):
    """Persistor class for Application model."""

    _search_table = Application

    def __init__(
        self,
        session: AsyncSession,
        application_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize ApplicationPersistor.

        Args:
            session: Async database session.
            application_search: Search system for applications.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = application_search
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find applications based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Application)  # Use select for async
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create async query."""
        return select(self.search_system.config.table)

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for applications.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = await self._search_query()
        query = self._filter_tenant_uuid(query)
        return await self.search_system.search_from_query(
            self.session, query, parameters
        )

    async def get_by(self, criteria: dict[str, Any]) -> Application:
        """Retrieve a single application by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Application: The found application.

        Raises:
            NotFoundError: If no application is found.

        """
        application = await self.find_by(criteria)
        if not application:
            msg = "Application"
            raise errors.NotFoundError(msg, **criteria)
        return application

    def _filter_tenant_uuid(self, query: Any) -> Any:
        """Filter query by tenant UUID.

        Args:
            query: The query object.

        Returns:
            The filtered query object.

        """
        if self.tenant_uuids is not None:
            query = query.filter(Application.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Application]:
        """Find all Application by criteria.

        Returns:
            list of Application.

        """
        result: Sequence[Application] = await super().find_all_by(criteria)
        return list(result)
