# file: accent_dao/resources/line/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.linefeatures import LineFeatures as Line
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.line.fixes import LineFixes
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

    from accent_dao.alchemy.application import Application
    from accent_dao.alchemy.endpoint_sip import EndpointSIP
    from accent_dao.alchemy.sccpline import SCCPLine
    from accent_dao.alchemy.usercustom import UserCustom

logger = logging.getLogger(__name__)


class LinePersistor(CriteriaBuilderMixin, AsyncBasePersistor[Line]):
    """Persistor class for Line model."""

    _search_table = Line

    def __init__(
        self, session: AsyncSession, tenant_uuids: list[str] | None = None
    ) -> None:
        """Initialize LinePersistor."""
        super().__init__(session, self._search_table)
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find lines based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Line)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> Line:
        """Retrieve a single line by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Line: The found line.

        Raises:
            NotFoundError: If no line is found.

        """
        line = await self.find_by(criteria)
        if not line:
            msg = "Line"
            raise errors.NotFoundError(msg, **criteria)
        return line

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for lines.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        # Assuming search_system is available, e.g., via a mixin or composition
        query = await self._search_query()
        query = self._filter_tenant_uuid(query)
        rows, total = await self.search_system.async_search_from_query(
            self.session, query, parameters
        )
        return SearchResult(total, rows)

    async def _search_query(self) -> Any:
        """Create a query for searching lines."""
        return select(self.search_system.config.table)

    def _filter_tenant_uuid(self, query: Any) -> Any:
        """Filter query by tenant UUID.

        Args:
            query: The query object.

        Returns:
            The filtered query object.

        """
        if self.tenant_uuids is not None:
            query = query.filter(Line.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def create(self, line: Line) -> Line:
        """Create a new line.

        Args:
            line: The line object.

        Returns:
            The created line object.

        """
        if line.provisioning_code is None:
            line.provisioning_code = self.generate_provisioning_code()
        if line.configregistrar is None:
            line.configregistrar = "default"
        if line.ipfrom is None:
            line.ipfrom = ""
        return await super().create(line)

    async def edit(self, line: Line) -> None:
        """Edit an existing line.

        Args:
            line: The line object to edit.

        """
        await super().edit(line)
        await LineFixes(self.session).async_fix(line.id)

    async def delete(self, line: Line) -> None:
        """Delete a line.

        Args:
            line: The line object to delete.

        """
        await super().delete(line)

    async def associate_endpoint_sip(self, line: Line, endpoint: EndpointSIP) -> None:
        """Associate a line with a SIP endpoint.

        Args:
            line: The line object.
            endpoint: The endpoint object.

        Raises:
            ResourceError: If the line already has an associated endpoint of a different type.

        """
        if line.protocol not in ("sip", None):
            raise errors.ResourceError(
                "Trunk", "Endpoint", line_id=line.id, protocol=line.protocol
            )
        line.endpoint_sip_uuid = endpoint.uuid
        await self.session.flush()

    async def dissociate_endpoint_sip(self, line: Line, endpoint: EndpointSIP) -> None:
        """Dissociate a line from a SIP endpoint.

        Args:
            line: The line object.
            endpoint: The endpoint object.

        """
        if endpoint is line.endpoint_sip:
            line.endpoint_sip_uuid = None
            await self.session.flush()

    async def associate_endpoint_sccp(self, line: Line, endpoint: SCCPLine) -> None:
        """Associate a line with an SCCP endpoint.

        Args:
            line: The line object.
            endpoint: The endpoint object.

        Raises:
            ResourceError: If the line already has an associated endpoint of a different type.

        """
        if line.protocol not in ("sccp", None):
            raise errors.ResourceError(
                "Trunk", "Endpoint", line_id=line.id, protocol=line.protocol
            )
        line.endpoint_sccp_id = endpoint.id
        await self.session.flush()

    async def dissociate_endpoint_sccp(self, line: Line, endpoint: SCCPLine) -> None:
        """Dissociate a line from an SCCP endpoint.

        Args:
            line: The line object.
            endpoint: The endpoint object.

        """
        if endpoint is line.endpoint_sccp:
            line.endpoint_sccp_id = None
            await self.session.flush()

    async def associate_endpoint_custom(self, line: Line, endpoint: UserCustom) -> None:
        """Associate a line with a custom endpoint.

        Args:
            line: The line object.
            endpoint: The endpoint object.

        Raises:
            ResourceError: If the line already has an associated endpoint of a different type.

        """
        if line.protocol not in ("custom", None):
            raise errors.ResourceError(
                "Trunk", "Endpoint", line_id=line.id, protocol=line.protocol
            )
        line.endpoint_custom_id = endpoint.id
        await self.session.flush()

    async def dissociate_endpoint_custom(self, line: Line, endpoint: UserCustom) -> None:
        """Dissociate a line from a custom endpoint.

        Args:
            line: The line object.
            endpoint: The endpoint object.

        """
        if endpoint is line.endpoint_custom:
            line.endpoint_custom_id = None
            await self.session.flush()

    async def associate_application(
        self, line: Line, application: Application
    ) -> None:
        """Associate a line with an application.

        Args:
            line: The line object.
            application: The application object.

        """
        line.application_uuid = application.uuid
        await self.session.flush()

    async def dissociate_application(
        self, line: Line, application: Application
    ) -> None:
        """Dissociate a line from an application.

        Args:
            line: The line object.
            application: The application object.

        """
        line.application_uuid = None
        await self.session.flush()

    def generate_provisioning_code(self) -> str:
        """Generate a provisioning code.

        Returns:
            str: The generated provisioning code.

        """
        # Keep this synchronous since it's used for default value generation
        while True:
            code = str(100000 + random.randint(0, 899999))
            # We can use the synchronous self.session here because we are *not* in an async function.
            if (
                not self.session.query(Line)
                .filter(Line.provisioningid == int(code))
                .first()
            ):
                return code

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Line]:
        """Find all lines by given criteria.

        Args:
            criteria (dict): Dictionary of criteria to filter by.

        Returns:
            list[Line]: List of Line objects.

        """
        result: Sequence[Line] = await super().find_all_by(criteria)
        return list(result)
