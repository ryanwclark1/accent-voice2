# file: accent_dao/resources/external_app/persistor.py
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.external_app import ExternalApp
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ExternalAppPersistor(CriteriaBuilderMixin, AsyncBasePersistor[ExternalApp]):
    """Persistor class for ExternalApp model."""

    _search_table = ExternalApp

    def __init__(
        self,
        session: AsyncSession,
        search_system: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize ExternalAppPersistor.

        Args:
            session: Async database session.
            search_system: Search system for ExternalApps.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = search_system
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find external apps based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(ExternalApp)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> ExternalApp:
        """Retrieve a single external app by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            ExternalApp: The found external app.

        Raises:
            NotFoundError: If no external app is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("ExternalApp", **criteria)
        return model

    async def _search_query(self) -> Any:
        """Create a query for searching external apps.

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
            query = query.filter(ExternalApp.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def find_all_by(self, criteria: dict[str, Any]) -> list[ExternalApp]:
        """Find all ExternalApp by criteria.

        Returns:
            list of ExternalApp.

        """
        result: Sequence[ExternalApp] = await super().find_all_by(criteria)
        return list(result)
