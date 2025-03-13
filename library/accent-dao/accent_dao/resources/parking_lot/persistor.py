# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.parking_lot import ParkingLot
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence


class ParkingLotPersistor(CriteriaBuilderMixin, AsyncBasePersistor[ParkingLot]):
    """Persistor class for ParkingLot model."""

    _search_table = ParkingLot

    def __init__(
        self,
        session: AsyncSession,
        parking_lot_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize ParkingLotPersistor.

        Args:
            session: Async database session.
            parking_lot_search: Search system for parking lots.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = parking_lot_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find parking lots based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(ParkingLot)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching parking lots."""
        return select(self.search_system.config.table)

    async def get_by(self, criteria: dict[str, Any]) -> ParkingLot:
        """Retrieve a single parking lot by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            ParkingLot: The found parking lot.

        Raises:
            NotFoundError: If no parking lot is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("ParkingLot", **criteria)
        return model

    async def find_all_by(self, criteria: dict[str, Any]) -> list[ParkingLot]:
        """Find all ParkingLot by criteria.

        Returns:
            list of ParkingLot.

        """
        result: Sequence[ParkingLot] = await super().find_all_by(criteria)
        return list(result)
