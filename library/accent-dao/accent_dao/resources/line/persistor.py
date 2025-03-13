# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from accent_dao.alchemy.linefeatures import LineFeatures
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import (
    CriteriaBuilderMixin,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from accent_dao.alchemy.application import Application
    from accent_dao.alchemy.endpoint_sip import EndpointSIP
    from accent_dao.alchemy.sccpline import SCCPLine
    from accent_dao.alchemy.usercustom import UserCustom


class LinePersistor(CriteriaBuilderMixin, AsyncBasePersistor[LineFeatures]):
    """Persistor class for LineFeatures model."""

    _search_table = LineFeatures

    def __init__(
        self,
        session: AsyncSession,
        line_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize LinePersistor.

        Args:
            session: Async database session.
            line_search: Search system for lines.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = line_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find lines based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(LineFeatures)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> LineFeatures:
        """Retrieve a single line by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            LineFeatures: The found line.

        Raises:
            NotFoundError: If no line is found.

        """
        line = await self.find_by(criteria)
        if not line:
            raise errors.NotFoundError("Line", **criteria)
        return line

    async def find_all_by(self, criteria: dict[str, Any]) -> list[LineFeatures]:
        """Find all LineFeatures by criteria.

        Returns:
            list of LineFeatures.

        """
        result: Sequence[LineFeatures] = await super().find_all_by(criteria)
        return list(result)

    async def associate_endpoint_sip(
        self, line: LineFeatures, endpoint: "EndpointSIP"
    ) -> None:
        """Associate a SIP endpoint with a line.

        Args:
            line: The line object.
            endpoint: The SIP endpoint object.

        Raises:
            ResourceError: If the line already has an associated endpoint of a different type.

        """
        if line.protocol not in ("sip", None):
            raise errors.ResourceError(
                "Line", "Endpoint", line_id=line.id, protocol=line.protocol
            )
        line.endpoint_sip_uuid = endpoint.uuid
        await self.session.flush()

    async def dissociate_endpoint_sip(
        self, line: LineFeatures, endpoint: "EndpointSIP"
    ) -> None:
        """Dissociate a SIP endpoint from a line.

        Args:
            line: The line object.
            endpoint: The SIP endpoint object.

        """
        if endpoint is line.endpoint_sip:
            line.endpoint_sip_uuid = None
            await self.session.flush()

    async def associate_endpoint_sccp(
        self, line: LineFeatures, endpoint: "SCCPLine"
    ) -> None:
        """Associate an SCCP endpoint with a line.

        Args:
            line: The line object.
            endpoint: The SCCP endpoint object.

        Raises:
            ResourceError: If the line already has an associated endpoint of a different type.

        """
        if line.protocol not in ("sccp", None):
            raise errors.ResourceError(
                "Line", "Endpoint", line_id=line.id, protocol=line.protocol
            )
        line.endpoint_sccp_id = endpoint.id
        await self.session.flush()

    async def dissociate_endpoint_sccp(
        self, line: LineFeatures, endpoint: "SCCPLine"
    ) -> None:
        """Dissociate an SCCP endpoint from a line.

        Args:
            line: The line object.
            endpoint: The SCCP endpoint object.

        """
        if endpoint is line.endpoint_sccp:
            line.endpoint_sccp_id = None
            await self.session.flush()

    async def associate_endpoint_custom(
        self, line: LineFeatures, endpoint: "UserCustom"
    ) -> None:
        """Associate a custom endpoint with a line.

        Args:
            line: The line object.
            endpoint: The custom endpoint object.

        Raises:
            ResourceError: If the line already has an associated endpoint of a different type.

        """
        if line.protocol not in ("custom", None):
            raise errors.ResourceError(
                "Line", "Endpoint", line_id=line.id, protocol=line.protocol
            )
        line.endpoint_custom_id = endpoint.id
        await self.session.flush()

    async def dissociate_endpoint_custom(
        self, line: LineFeatures, endpoint: "UserCustom"
    ) -> None:
        """Dissociate a custom endpoint from a line.

        Args:
            line: The line object.
            endpoint: The custom endpoint object.

        """
        if endpoint is line.endpoint_custom:
            line.endpoint_custom_id = None
            await self.session.flush()

    async def associate_application(
        self, line: LineFeatures, application: "Application"
    ) -> None:
        """Associate an application with a line.

        Args:
            line: The line object.
            application: The application object.

        """
        line.application_uuid = application.uuid
        await self.session.flush()

    async def dissociate_application(
        self, line: LineFeatures, application: "Application"
    ) -> None:
        """Dissociate an application from a line.

        Args:
            line: The line object.
            application: The application object.

        """
        if application is line.application:
            line.application_uuid = None
            await self.session.flush()
