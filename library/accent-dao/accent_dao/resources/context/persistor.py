# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.context import Context
from accent_dao.alchemy.contextinclude import ContextInclude
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


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
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = context_search

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
        """Create a query for searching contexts."""
        return select(self.search_system.config.table)

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
            raise errors.NotFoundError("Context", **criteria)
        return context

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Context]:
        """Find all Context by criteria.

        Returns:
            list of Context.

        """
        result: Sequence[Context] = await super().find_all_by(criteria)
        return list(result)

    async def associate_contexts(
        self, context: Context, included_contexts: list[str]
    ) -> None:
        """Associate contexts within context.

        Args:
            context: Context to associate.
            included_contexts: Contexts to be associated.

        """
        context.contexts = included_contexts
        await self.session.flush()
