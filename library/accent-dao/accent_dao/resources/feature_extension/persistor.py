# file: accent_dao/resources/feature_extension/persistor.py
# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.feature_extension import FeatureExtension
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin, SearchResult

if TYPE_CHECKING:
    from collections.abc import Sequence

from .database import (
    AgentActionFeatureExtension,
    ForwardFeatureExtension,
    ServiceFeatureExtension,
    agent_action_converter,
    fwd_converter,
    service_converter,
)

logger = logging.getLogger(__name__)


class FeatureExtensionPersistor(
    CriteriaBuilderMixin, AsyncBasePersistor[FeatureExtension]
):
    """Persistor class for FeatureExtension model."""

    _search_table = FeatureExtension

    def __init__(self, session: AsyncSession) -> None:
        """Initialize FeatureExtensionPersistor.

        Args:
            session: Async database session.

        """
        super().__init__(session, self._search_table)
        self.session = session

    async def _find_query(self, criteria: dict[str, Any]) -> Any:
        """Build a query to find feature extensions based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(FeatureExtension)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict[str, Any]) -> FeatureExtension:
        """Retrieve a single feature extension by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            FeatureExtension: The found feature extension.

        Raises:
            NotFoundError: If no feature extension is found.

        """
        model = await self.find_by(criteria)
        if not model:
            raise errors.NotFoundError("FeatureExtension", **criteria)
        return model

    async def search(self, parameters: dict[str, Any]) -> SearchResult:
        """Search for feature extensions.

        Args:
            parameters: Search parameters.

        Returns:
            SearchResult object containing total count and items.

        """
        query = await self._search_query()
        rows, total = await feature_extension_search.async_search_from_query(
            self.session, query, parameters
        )
        return SearchResult(total, rows)

    async def _search_query(self) -> Any:
        """Create a query for searching feature extensions.

        Returns:
            SQLAlchemy query object.

        """
        return select(feature_extension_search.config.table)

    async def find_all_by(self, criteria: dict[str, Any]) -> list[FeatureExtension]:
        """Find all FeatureExtension by criteria.

        Returns:
            list of FeatureExtension.

        """
        result: Sequence[FeatureExtension] = await super().find_all_by(criteria)
        return list(result)

    async def find_all_service_extensions(
        self,
    ) -> list[ServiceFeatureExtension]:
        """Find all service feature extensions.

        Returns:
            A list of ServiceFeatureExtension objects.

        """
        features = service_converter.features()
        query = select(
            FeatureExtension.uuid, FeatureExtension.exten, FeatureExtension.feature
        ).filter(FeatureExtension.feature.in_(features))

        result = await self.session.execute(query)
        return [service_converter.to_model(row) for row in result.all()]

    async def find_all_forward_extensions(self) -> list[ForwardFeatureExtension]:
        """Find all forward feature extensions.

        Returns:
            A list of ForwardFeatureExtension objects.

        """
        features = fwd_converter.features()
        query = select(
            FeatureExtension.uuid, FeatureExtension.exten, FeatureExtension.feature
        ).filter(FeatureExtension.feature.in_(features))

        result = await self.session.execute(query)
        return [fwd_converter.to_model(row) for row in result.all()]

    async def find_all_agent_action_extensions(
        self,
    ) -> list[AgentActionFeatureExtension]:
        """Find all agent action feature extensions.

        Returns:
            A list of AgentActionFeatureExtension objects.

        """
        features = agent_action_converter.features()
        query = select(
            FeatureExtension.uuid, FeatureExtension.exten, FeatureExtension.feature
        ).filter(FeatureExtension.feature.in_(features))

        result = await self.session.execute(query)
        return [agent_action_converter.to_model(row) for row in result.all()]
