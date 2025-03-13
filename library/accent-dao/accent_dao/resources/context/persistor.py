# file: accent_dao/resources/context/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.context import Context
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class ContextPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Context]):
    """Persistor class for Context model."""

    _search_table = Context

    def __init__(
        self,
        session: AsyncSession,
        context_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize ContextPersistor.

        Args:
            session: Async database session.
            context_search: Search system for contexts.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = context_search
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find contexts based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Context)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching contexts.

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
            query = query.filter(Context.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for Contexts.

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

    async def get_by(self, criteria: dict[str, Any]) -> Context:
        """Retrieve a single context by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Context: The found context.

        Raises:
            NotFoundError: If no context is found.

        """
        context = await self.find_by(criteria)
        if not context:
            msg = "Context"
            raise errors.NotFoundError(msg, **criteria)
        return context

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Context]:
        """Find all Context by criteria.

        Returns:
            list of Contexts.

        """
        result: Sequence[Context] = await super().find_all_by(criteria)
        return list(result)

    async def associate_contexts(self, context: Context, contexts: list[str]) -> None:
        """Associate a list of contexts.

        Args:
            context: Main context to be associated.
            contexts: List of contexts to associate with the main context.

        """
        context.contexts = contexts
        await self.session.flush()
