# file: accent_dao/resources/endpoint_sccp/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.sccpline import SCCPLine as SCCP  # noqa: N814
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.line.fixes import LineFixes
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)


class SCCPPersistor(CriteriaBuilderMixin, AsyncBasePersistor[SCCP]):
    """Persistor class for SCCPLine model."""

    _search_table = SCCP

    def __init__(
        self,
        session: AsyncSession,
        sccp_search: Any,  # Use Any for now; specify more accurately if possible
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize SCCPPersistor.

        Args:
            session: Async database session.
            sccp_search: Search system for SCCP endpoints.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = sccp_search
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find SCCP endpoints based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(SCCP)  # Use select for async
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> SCCP:
        """Retrieve a single SCCP endpoint by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SCCP: The found SCCP endpoint.

        Raises:
            NotFoundError: If no SCCP endpoint is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("SCCPEndpoint", **criteria)
        return model

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for SCCP endpoints.

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
        """Create a query for searching SCCP endpoints.

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
            query = query.filter(SCCP.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def create(self, sccp: SCCP) -> SCCP:
        """Create a new SCCP endpoint.

        Args:
            sccp: The SCCP endpoint object to create.

        Returns:
            The created SCCP endpoint object.

        """
        return await super().create(sccp)

    async def edit(self, sccp: SCCP) -> None:
        """Edit an existing SCCP endpoint.

        Args:
            sccp: The SCCP endpoint object to edit.

        """
        await super().edit(sccp)
        await self.async_fix_associated(sccp)

    async def delete(self, sccp: SCCP) -> None:
        """Delete an SCCP endpoint.

        Args:
            sccp: The SCCP endpoint object to delete.

        """
        await super().delete(sccp)
        await self.async_fix_associated(sccp)

    async def async_fix_associated(self, sccp: SCCP) -> None:
        """Fix associated line after edit or delete.

        Args:
            sccp: The SCCP endpoint instance.

        """
        if sccp.line:
            await LineFixes(self.session).async_fix(sccp.line.id)

    async def find_all_by(self, criteria: dict[str, Any]) -> list[SCCP]:
        """Find all SCCP by criteria.

        Returns:
            list of SCCP.

        """
        result: Sequence[SCCP] = await super().find_all_by(criteria)
        return list(result)
