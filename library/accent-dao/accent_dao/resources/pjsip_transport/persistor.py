# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from accent_dao.alchemy.endpoint_sip import EndpointSIP
from accent_dao.alchemy.pjsip_transport import PJSIPTransport
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class PJSIPTransportPersistor(CriteriaBuilderMixin, AsyncBasePersistor[PJSIPTransport]):
    """Persistor class for PJSIPTransport model."""

    _search_table = PJSIPTransport

    def __init__(self, session: AsyncSession, transport_search: Any) -> None:
        """Initialize PJSIPTransportPersistor.

        Args:
            session: Async database session.
            transport_search: Search system for PJSIP transports.

        """
        super().__init__(session, self._search_table)
        self.search_system = transport_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find PJSIP transports based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(PJSIPTransport)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> PJSIPTransport:
        """Retrieve a single PJSIP transport by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            PJSIPTransport: The found PJSIP transport.

        Raises:
            NotFoundError: If no PJSIP transport is found.

        """
        transport = await self.find_by(criteria)
        if not transport:
            raise errors.NotFoundError("Transport", **criteria)
        return transport

    async def find_all_by(self, criteria: dict[str, Any]) -> list[PJSIPTransport]:
        """Find all PJSIPTransport by criteria.

        Returns:
            list of PJSIPTransport.

        """
        result: Sequence[PJSIPTransport] = await super().find_all_by(criteria)
        return list(result)

    async def delete(
        self, transport: PJSIPTransport, fallback: PJSIPTransport | None = None
    ) -> None:
        """Delete a PJSIP transport and reassign endpoints to a fallback.

        Args:
            transport: The PJSIPTransport object to delete.
            fallback: An optional fallback transport to reassign endpoints to.

        """
        if fallback:
            await self._update_transport(transport, fallback)
        await super().delete(transport)

    async def _update_transport(
        self, current: PJSIPTransport, new: PJSIPTransport
    ) -> None:
        """Reassign endpoints from one transport to another.

        Args:
            current: The current PJSIPTransport.
            new: The new PJSIPTransport.

        """
        stmt = (
            update(EndpointSIP)
            .where(EndpointSIP.transport_uuid == current.uuid)
            .values(transport_uuid=new.uuid)
        )
        await self.session.execute(stmt)
