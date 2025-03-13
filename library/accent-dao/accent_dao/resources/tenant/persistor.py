# file: accent_dao/resources/tenant/persistor.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.tenant import Tenant
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class TenantPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Tenant]):
    """Persistor class for Tenant model."""

    _search_table = Tenant

    def __init__(
        self,
        session: AsyncSession,
        search_system: Any,  # Use Any for SearchSystem for now
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize TenantPersistor.

        Args:
            session: Async database session.
            search_system: Search system for tenants.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = search_system
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find tenants based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Tenant)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> Tenant:
        """Retrieve a single tenant by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Tenant: The found tenant.

        Raises:
            NotFoundError: If no tenant is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("Tenant", **criteria)
        return model

    async def _search_query(self) -> Any:
        """Create a query for searching tenants.

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
            query = query.filter(Tenant.uuid.in_(self.tenant_uuids))
        return query

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Tenant]:
        """Find all Tenant by criteria.

        Returns:
            list of Tenant.

        """
        result: Sequence[Tenant] = await super().find_all_by(criteria)
        return list(result)
