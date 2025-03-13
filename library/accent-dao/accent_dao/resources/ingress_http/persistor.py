# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.ingress_http import IngressHTTP
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class IngressHTTPPersistor(CriteriaBuilderMixin, AsyncBasePersistor[IngressHTTP]):
    """Persistor class for IngressHTTP model."""

    _search_table = IngressHTTP

    def __init__(
        self,
        session: AsyncSession,
        ingress_http_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize IngressHTTPPersistor.

        Args:
            session: Async database session.
            ingress_http_search: Search system for HTTP ingresses.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = ingress_http_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find HTTP ingresses based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(IngressHTTP)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching HTTP ingresses."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> IngressHTTP:
        """Retrieve a single HTTP ingress by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            IngressHTTP: The found HTTP ingress.

        Raises:
            NotFoundError: If no HTTP ingress is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("IngressHTTP", **criteria)
        return model

    async def find_all_by(self, criteria: dict[str, Any]) -> list[IngressHTTP]:
        """Find all IngressHTTP by criteria.

        Returns:
            list of IngressHTTP.

        """
        result: Sequence[IngressHTTP] = await super().find_all_by(criteria)
        return list(result)
