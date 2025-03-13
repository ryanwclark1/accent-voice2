# file: accent_dao/resources/voicemail/persistor.py
# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.voicemail import Voicemail
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class VoicemailPersistor(CriteriaBuilderMixin, AsyncBasePersistor[Voicemail]):
    """Persistor class for Voicemail model."""

    _search_table = Voicemail

    def __init__(
        self,
        session: AsyncSession,
        voicemail_search: Any,
        tenant_uuids: list[str] | None = None,
    ) -> None:
        """Initialize VoicemailPersistor.

        Args:
            session: Async database session.
            voicemail_search: Search system for voicemails.
            tenant_uuids: Optional list of tenant UUIDs to filter by.

        """
        super().__init__(session, self._search_table)
        self.search_system = voicemail_search
        self.tenant_uuids = tenant_uuids
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find voicemails based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(Voicemail)
        query = self._filter_tenant_uuid(query)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> Voicemail:
        """Retrieve a single voicemail by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            Voicemail: The found voicemail.

        Raises:
            NotFoundError: If no voicemail is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("Voicemail", **criteria)
        return model

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for voicemails.

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

    async def _search_query(self) -> Any:
        """Create a query for searching voicemails.

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
            query = query.filter(Voicemail.tenant_uuid.in_(self.tenant_uuids))
        return query

    async def find_all_by(self, criteria: dict[str, Any]) -> list[Voicemail]:
        """Find all Voicemail by criteria.

        Returns:
            list of Voicemail.

        """
        result: Sequence[Voicemail] = await super().find_all_by(criteria)
        return list(result)
