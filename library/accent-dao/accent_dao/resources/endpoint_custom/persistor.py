# file: accent_dao/resources/endpoint_custom/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.usercustom import UserCustom as Custom
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.line.fixes import LineFixes
from accent_dao.resources.trunk.fixes import TrunkFixes
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class CustomPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Custom]):
    """Persistor class for Custom model."""

    _search_table = Custom

    def __init__(
        self,
        session: AsyncSession,
        search_system: Any,  # Use Any for now
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize CustomPersistor.

        Args:
            session: Async database session.
            search_system: Search system for custom endpoints.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = search_system
        self.tenant_uuids = tenant_uuids
        self.session = session  # Retain for use in custom methods

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find custom endpoints based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Custom)  # Use select for async
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching custom endpoints.

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
            query = query.filter(Custom.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Custom]:
        """Find all Custom by criteria.

        Returns:
            list of Custom.

        """
        result: Sequence[Custom] = await super().find_all_by(criteria)
        return list(result)

    async def get_by(self, criteria: dict[str, Any]) -> Custom:
        """Retrieve a single custom endpoint by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Custom: The found custom endpoint.

        Raises:
            NotFoundError: If no custom endpoint is found.

        """
        model = await self.find_by(criteria)
        if not model:
            msg = "CustomEndpoint"
            raise errors.NotFoundError(msg, **criteria)
        return model

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for custom endpoints.

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

    async def create(self, custom: Custom) -> Custom:
        """Create custom Endpoint."""
        self.fill_default_values(custom)
        return await super().create(custom)

    def fill_default_values(self, custom: Custom) -> None:
        """Fill default values for a custom endpoint.

        Args:
            custom: The custom endpoint object.

        """
        if custom.protocol is None:
            custom.protocol = "custom"
        if custom.category is None:
            custom.category = "user"

    async def edit(self, custom: Custom) -> None:
        """Edit an existing custom endpoint."""
        await super().edit(custom)
        await self._fix_associated(custom)

    async def delete(self, custom: Custom) -> None:
        """Delete a custom endpoint."""
        await super().delete(custom)
        await self._fix_associated(custom)

    async def _fix_associated(self, custom: Custom) -> None:
        """Fix associated line or trunk after edit or delete.

        Args:
            custom: The custom endpoint instance.

        """
        if custom.line:
            await LineFixes(self.session).async_fix(custom.line.id)

        if custom.trunk:
            await TrunkFixes(self.session).async_fix(custom.trunk.id)
