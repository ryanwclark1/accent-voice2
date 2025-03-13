# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.ivr import IVR
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence
    from accent_dao.alchemy.dialaction import Dialaction


class IVRPersistor(CriteriaBuilderMixin, AsyncBasePersistor[IVR]):
    """Persistor class for IVR model."""

    _search_table = IVR

    def __init__(
        self,
        session: AsyncSession,
        ivr_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize IVRPersistor.

        Args:
            session: Async database session.
            ivr_search: Search system for IVRs.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table, tenant_uuids)
        self.search_system = ivr_search

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find IVRs based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(IVR)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> IVR:
        """Retrieve a single IVR by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            IVR: The found IVR.

        Raises:
            NotFoundError: If no IVR is found.

        """
        ivr = await self.find_by(criteria)
        if not ivr:
            raise errors.NotFoundError("IVR", **criteria)
        return ivr

    async def find_all_by(self, criteria: dict[str, Any]) -> list[IVR]:
        """Find all IVR by criteria.

        Returns:
            list of IVR.

        """
        result: Sequence[IVR] = await super().find_all_by(criteria)
        return list(result)

    async def update_dialaction(
        self, ivr: IVR, event: str, dialaction: "Dialaction"
    ) -> None:
        """Update the destination dialaction of an IVR.

        Args:
            ivr: The IVR object to be updated
            event: The event where to find the dialaction
            dialaction: The new Dialaction.

        """
        setattr(ivr, f"{event}_destination", dialaction)
        await self.session.flush()
