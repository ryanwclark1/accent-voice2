# file: accent_dao/resources/access_feature/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.accessfeatures import AccessFeatures
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence


class AccessFeaturesPersistor(CriteriaBuilderMixin, AsyncBasePersistor):
    """Persistor class for AccessFeatures model."""

    _search_table = AccessFeatures

    def __init__(self, session: AsyncSession, access_feature_search: Any) -> None:
        """Initialize AccessFeaturesPersistor.

        Args:
            session: Async database session.
            access_feature_search: Search system for access features.

        """
        super().__init__(session, self._search_table)
        self.access_feature_search = access_feature_search
        self.session = session  # Keep this for now

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find access features based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(AccessFeatures)
        return self.build_criteria(query, criteria)

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for access features.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = select(self.access_feature_search.config.table)
        return await self.access_feature_search.search_from_query(
            self.session, query, parameters
        )

    async def get_by(self, criteria: dict[str, Any]) -> AccessFeatures:
        """Retrieve a single access feature by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            AccessFeatures: The found access feature.

        Raises:
            NotFoundError: If no access feature is found.

        """
        model = await self.find_by(criteria)
        if not model:
            msg = "AccessFeature"
            raise errors.NotFoundError(msg, **criteria)
        return model

    async def find_all_by(self, criteria: dict[str, Any]) -> list[AccessFeatures]:
        """Find all AccessFeatures by criteria.

        Returns:
            list of AccessFeatures.

        """
        result: Sequence[AccessFeatures] = await super().find_all_by(criteria)
        return list(result)
