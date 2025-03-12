# file: accent_dao/resources/call_permission/persistor.py
# Copyright 2025 Accent Communications
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from accent_dao.alchemy.rightcall import RightCall as CallPermission
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.query_options import QueryOptionsMixin
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession


class CallPermissionPersistor(
    QueryOptionsMixin, CriteriaBuilderMixin, AsyncBasePersistor[CallPermission]
):
    """Persistor class for CallPermission model."""

    _search_table = CallPermission

    def __init__(
        self,
        session: AsyncSession,
        call_permission_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        super().__init__(session, self._search_table)
        """Initialize CallPermissionPersistor.

        Args:
            session: Async database session.
            call_permission_search: Search system for call permissions.
            tenant_uuids: Optional list of tenant UUIDs to filter by.
        """
        self.search_system = call_permission_search
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def get_by(self, criteria: dict[str, Any]) -> CallPermission:
        """Retrieve a single call permission by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            CallPermission: The found call permission.

        Raises:
            NotFoundError: If no call permission is found.
        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("CallPermission", **criteria)
        return model

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find call permissions based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.
        """
        query = select(CallPermission)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching call permissions.

        Returns:
            SQLAlchemy query object.
        """
        query = select(self.search_system.config.table)
        query = self._apply_query_options(query)
        return query

    def _filter_tenant_uuid(self, query: Any) -> Any:
        """Filter query by tenant UUID.

        Args:
            query: The query object.

        Returns:
            The filtered query object.
        """
        if self.tenant_uuids is not None:
            query = query.filter(CallPermission.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def find_all_by(self, criteria: dict[str, Any]) -> list[CallPermission]:
        """Find all CallPermission by criteria.

        Returns:
            list of CallPermission.
        """
        result: Sequence[CallPermission] = await super().find_all_by(criteria)
        return list(result)
