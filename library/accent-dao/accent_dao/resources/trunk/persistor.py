# file: accent_dao/resources/trunk/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.trunkfeatures import TrunkFeatures as Trunk
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.trunk.fixes import TrunkFixes
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

    from accent_dao.alchemy.endpoint_sip import EndpointSIP
    from accent_dao.alchemy.staticiax import StaticIAX
    from accent_dao.alchemy.usercustom import UserCustom
    from accent_dao.alchemy.useriax import UserIAX

logger = logging.getLogger(__name__)


class TrunkPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Trunk]):
    """Persistor class for Trunk model."""

    _search_table = Trunk

    def __init__(
        self,
        session: AsyncSession,
        trunk_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize TrunkPersistor.

        Args:
            session: Async database session.
            trunk_search: Search system for trunks.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = trunk_search
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find trunks based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Trunk)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching trunks.

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
            query = query.filter(Trunk.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def get_by(self, criteria: dict[str, Any]) -> Trunk:
        """Retrieve a single trunk by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Trunk: The found trunk.

        Raises:
            NotFoundError: If no trunk is found.

        """
        trunk = await self.find_by(criteria)
        if not trunk:
            raise errors.NotFoundError("Trunk", **criteria)
        return trunk

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for trunks.

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

    async def edit(self, trunk: Trunk) -> None:
        """Edit an existing trunk."""
        await super().edit(trunk)
        await TrunkFixes(self.session).async_fix(trunk.id)

    async def associate_endpoint_sip(self, trunk: Trunk, endpoint: EndpointSIP) -> None:
        """Associate a trunk with a SIP endpoint.

        Args:
            trunk: The trunk object.
            endpoint: The SIP endpoint object.

        """
        if trunk.protocol not in ("sip", None):
            raise errors.ResourceError(
                "Trunk", "Endpoint", trunk_id=trunk.id, protocol=trunk.protocol
            )
        trunk.endpoint_sip_uuid = endpoint.uuid
        await self.session.flush()

    async def dissociate_endpoint_sip(
        self, trunk: Trunk, endpoint: EndpointSIP
    ) -> None:
        """Dissociate a trunk from a SIP endpoint.

        Args:
            trunk: The trunk object.
            endpoint: The SIP endpoint object.

        """
        if endpoint is trunk.endpoint_sip:
            trunk.endpoint_sip_uuid = None
            await self.session.flush()

    async def associate_endpoint_iax(self, trunk: Trunk, endpoint: UserIAX) -> None:
        """Associate a trunk with an IAX endpoint.

        Args:
            trunk: The trunk object.
            endpoint: The IAX endpoint object.

        """
        if trunk.protocol not in ("iax", None):
            raise errors.ResourceError(
                "Trunk", "Endpoint", trunk_id=trunk.id, protocol=trunk.protocol
            )
        trunk.endpoint_iax_id = endpoint.id
        await self.session.flush()

    async def dissociate_endpoint_iax(self, trunk: Trunk, endpoint: UserIAX) -> None:
        """Dissociate a trunk from an IAX endpoint.

        Args:
            trunk: The trunk object.
            endpoint: The IAX endpoint object.

        """
        if endpoint is trunk.endpoint_iax:
            trunk.endpoint_iax_id = None
            await self.session.flush()

    async def associate_endpoint_custom(
        self, trunk: Trunk, endpoint: UserCustom
    ) -> None:
        """Associate a trunk with a custom endpoint.

        Args:
            trunk: The trunk object.
            endpoint: The custom endpoint object.

        """
        if trunk.protocol not in ("custom", None):
            raise errors.ResourceError(
                "Trunk", "Endpoint", trunk_id=trunk.id, protocol=trunk.protocol
            )
        trunk.endpoint_custom_id = endpoint.id
        await self.session.flush()

    async def dissociate_endpoint_custom(
        self, trunk: Trunk, endpoint: UserCustom
    ) -> None:
        """Dissociate a trunk from a custom endpoint.

        Args:
            trunk: The trunk object.
            endpoint: The custom endpoint object.

        """
        if endpoint is trunk.endpoint_custom:
            trunk.endpoint_custom_id = None
            await self.session.flush()

    async def associate_register_iax(self, trunk: Trunk, register: StaticIAX) -> None:
        """Associate a trunk with a register IAX.

        Args:
            trunk: The trunk object.
            register: The register IAX object.

        """
        if trunk.protocol not in ("iax", None):
            raise errors.ResourceError(
                "Trunk", "Endpoint", trunk_id=trunk.id, protocol=trunk.protocol
            )
        trunk.register_iax_id = register.id
        await self.session.flush()

    async def dissociate_register_iax(self, trunk: Trunk, register: StaticIAX) -> None:
        """Dissociate a trunk from a register IAX.

        Args:
            trunk: The trunk object.
            register: The register IAX object.

        """
        if register is trunk.register_iax:
            trunk.register_iax_id = None
            await self.session.flush()

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Trunk]:
        """Find all Trunk by criteria.

        Returns:
            list of Trunk.

        """
        result: Sequence[Trunk] = await super().find_all_by(criteria)
        return list(result)
