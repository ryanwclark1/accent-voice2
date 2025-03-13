# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.meeting_authorization import MeetingAuthorization
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class MeetingAuthorizationPersistor(
    CriteriaBuilderMixin, AsyncBasePersistor[MeetingAuthorization]
):
    """Persistor class for MeetingAuthorization model."""

    _search_table = MeetingAuthorization

    def __init__(
        self,
        session: AsyncSession,
        meeting_authorization_search: Any,
        meeting_uuid: str | None = None,
    ) -> None:
        """Initialize MeetingAuthorizationPersistor.

        Args:
            session: Async database session.
            meeting_authorization_search: Search system for meeting authorizations.
            meeting_uuid: Optional meeting UUID to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = meeting_authorization_search
        self.meeting_uuid = meeting_uuid

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find meeting authorizations based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(MeetingAuthorization)
        query = self._filter_meeting_uuid(query)
        return self.build_criteria(query, criteria)

    async def _search_query(self) -> Any:
        """Create a query for searching meeting authorizations."""
        query = select(self.search_system.config.table)
        query = self._filter_meeting_uuid(query)
        return query

    def _filter_meeting_uuid(self, query: Any) -> Any:
        """Filter query by meeting UUID.

        Args:
            query: SQLAlchemy query object

        Returns:
            Filtered query object

        """
        if self.meeting_uuid is None:
            return query
        return query.filter(MeetingAuthorization.meeting_uuid == self.meeting_uuid)

    async def get_by(self, criteria: dict[str, Any]) -> MeetingAuthorization:
        """Retrieve a single meeting authorization by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            MeetingAuthorization: The found meeting authorization.

        Raises:
            NotFoundError: If no meeting authorization is found.

        """
        model = await self.find_by(criteria)
        if not model:
            msg = "MeetingAuthorization"
            raise errors.NotFoundError(msg, **criteria)
        return model

    async def find_all_by(self, criteria: dict[str, Any]) -> list[MeetingAuthorization]:
        """Find all MeetingAuthorization by criteria.

        Returns:
            list of MeetingAuthorization.

        """
        result: Sequence[MeetingAuthorization] = await super().find_all_by(criteria)
        return list(result)
