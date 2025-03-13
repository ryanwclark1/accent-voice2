# file: accent_dao/resources/endpoint_iax/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.useriax import UserIAX as IAX
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.trunk.fixes import TrunkFixes
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class IAXPersistor(CriteriaBuilderMixin, AsyncBasePersistor[IAX]):
    """Persistor class for IAX model."""

    _search_table = IAX

    def __init__(
        self,
        session: AsyncSession,
        iax_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize IAXPersistor.

        Args:
            session: Async database session.
            iax_search: Search system for IAX endpoints.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = iax_search
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find IAX endpoints based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(IAX)  # Use select for async
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching IAX endpoints.

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
            query = query.filter(IAX.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def get_by(self, criteria: dict[str, Any]) -> IAX:
        """Retrieve a single IAX endpoint by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            IAX: The found IAX endpoint.

        Raises:
            NotFoundError: If no IAX endpoint is found.

        """
        iax = await self.find_by(criteria)
        if not iax:
            msg = "IAXEndpoint"
            raise errors.NotFoundError(msg, **criteria)
        return iax

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for IAX endpoints.

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

    async def create(self, iax: IAX) -> IAX:
        """Create a new IAX endpoint.

        Args:
            iax: The IAX endpoint object to create.

        Returns:
            The created IAX endpoint object.

        """
        self.fill_default_values(iax)
        return await super().create(iax)

    def fill_default_values(self, iax: IAX) -> None:
        """Fill default values for an IAX endpoint.

        Args:
            iax: The IAX endpoint object.

        """
        if iax.name is None:
            iax.name = self._generate_name()
        if iax.type is None:
            iax.type = "friend"
        if iax.host is None:
            iax.host = "dynamic"
        if iax.category is None:
            iax.category = "trunk"

    async def edit(self, iax: IAX) -> None:
        """Edit an existing IAX endpoint.

        Args:
            iax: The IAX endpoint object to edit.

        """
        await super().edit(iax)
        await self._fix_associated(iax)

    async def delete(self, iax: IAX) -> None:
        """Delete an IAX endpoint.

        Args:
            iax: The IAX endpoint object to delete.

        """
        await super().delete(iax)
        await self._fix_associated(iax)

    async def _fix_associated(self, iax: IAX) -> None:
        """Fix associated trunk after edit or delete.

        Args:
            iax: The IAX endpoint object.

        """
        if iax.trunk_rel:
            await TrunkFixes(self.session).async_fix(iax.trunk_rel.id)

    async def find_all_by(self, criteria: dict[str, Any]) -> list[IAX]:
        """Find all IAX by criteria.

        Returns:
            list of IAX.

        """
        result: Sequence[IAX] = await super().find_all_by(criteria)
        return list(result)
