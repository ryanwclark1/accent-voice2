# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.phone_number import PhoneNumber
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class PhoneNumberPersistor(CriteriaBuilderMixin, AsyncBasePersistor[PhoneNumber]):
    """Persistor class for PhoneNumber model."""

    _search_table = PhoneNumber

    def __init__(
        self,
        session: AsyncSession,
        phone_number_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize PhoneNumberPersistor.

        Args:
            session: Async database session.
            phone_number_search: Search system for phone numbers.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = phone_number_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find phone numbers based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(PhoneNumber)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching phone numbers."""
        query = select(self.search_system.config.table)
        query = self._filter_tenant_uuid(query)
        return query

    async def get_by(self, criteria: dict[str, Any]) -> PhoneNumber:
        """Retrieve a single phone number by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            PhoneNumber: The found phone number.

        Raises:
            NotFoundError: If no phone number is found.

        """
        phone_number = await self.find_by(criteria)
        if not phone_number:
            msg = "PhoneNumber"
            raise errors.NotFoundError(msg, **criteria)
        return phone_number

    async def find_all_by(self, criteria: dict[str, Any]) -> list[PhoneNumber]:
        """Find all PhoneNumber by criteria.

        Returns:
            list of PhoneNumber.

        """
        result: Sequence[PhoneNumber] = await super().find_all_by(criteria)
        return list(result)
