# file: accent_dao/resources/endpoint_sip/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.endpoint_sip import EndpointSIP
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.line.fixes import LineFixes
from accent_dao.resources.trunk.fixes import TrunkFixes
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class SIPPersistor(CriteriaBuilderMixin, AsyncBasePersistor[EndpointSIP]):
    """Persistor class for EndpointSIP model."""

    _search_table = EndpointSIP

    def __init__(
        self,
        session: AsyncSession,
        search_system: Any,  # Use Any for now
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize SIPPersistor.

        Args:
            session: Async database session.
            search_system: Search system for SIP endpoints.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = search_system
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find SIP endpoints based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(EndpointSIP)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> EndpointSIP:
        """Retrieve a single SIP endpoint by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            EndpointSIP: The found SIP endpoint.

        Raises:
            NotFoundError: If no SIP endpoint is found.

        """
        endpoint = await self.find_by(criteria)
        if not endpoint:
            msg = "SIPEndpoint"
            raise errors.NotFoundError(msg, **criteria)
        return endpoint

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for SIP endpoints.

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
        """Create a query for searching SIP endpoints.

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
            query = query.filter(EndpointSIP.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def create(self, sip: EndpointSIP) -> EndpointSIP:
        """Create a new SIP endpoint.

        Args:
            sip: The endpoint object to create.

        Returns:
            The created endpoint object.

        """
        self._fill_default_values(sip)
        return await super().create(sip)

    def _fill_default_values(self, sip: EndpointSIP) -> None:
        """Fill default values for a SIP endpoint.

        Args:
            sip: The endpoint object.

        """
        if sip.name is None:
            sip.name = self._generate_name()

    def _generate_name(self) -> str:
        """Generate a unique name for the SIP endpoint."""
        # This is a placeholder, a real implementation would need to ensure uniqueness.
        import uuid

        return str(uuid.uuid4())

    async def edit(self, sip: EndpointSIP) -> None:
        """Edit an existing SIP endpoint."""
        await super().edit(sip)
        await self._fix_associated(sip)

    async def delete(self, sip: EndpointSIP) -> None:
        """Delete a SIP endpoint."""
        await super().delete(sip)
        await self._fix_associated(sip)

    async def _fix_associated(self, sip: EndpointSIP) -> None:
        """Fix associated line or trunk after edit or delete.

        Args:
            sip: The EndpointSIP instance.

        """
        if sip.line:
            await LineFixes(self.session).async_fix(sip.line.id)

        if sip.trunk:
            await TrunkFixes(self.session).async_fix(sip.trunk.id)

    async def find_all_by(self, criteria: dict[str, Any]) -> list[EndpointSIP]:
        """Find all SIP endpoints by criteria.

        Returns:
            A list of EndpointSIP objects.

        """
        result: Sequence[EndpointSIP] = await super().find_all_by(criteria)
        return list(result)
