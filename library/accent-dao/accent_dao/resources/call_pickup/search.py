# /resources/call_pickup/search.py
# Copyright 2025 Accent Communications

import logging
from typing import Any

from accent_dao.alchemy.pickup import Pickup as CallPickup
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

logger = logging.getLogger(__name__)

# Configure the search for call pickups
config = SearchConfig(
    table=CallPickup,
    columns={
        "id": CallPickup.id,
        "name": CallPickup.name,
        "description": CallPickup.description,
        "enabled": CallPickup.enabled,
    },
    search=["name", "description"],
    default_sort="name",
)


class AsyncSearchSystem:
    """Search system with async support.

    Extends the base SearchSystem to provide async functionality.
    """

    def __init__(self, config: SearchConfig) -> None:
        """Initialize the AsyncSearchSystem.

        Args:
            config: Search configuration

        """
        self.config = config
        self._sync_search = SearchSystem(config)

    async def async_create_query(
        self, base_query: Any, parameters: dict[str, Any]
    ) -> Any:
        """Create an async query based on search parameters.

        Args:
            base_query: Base SQLAlchemy async query
            parameters: Search parameters

        Returns:
            SQLAlchemy async query object

        """
        # We build on top of the original SearchSystem for async operations
        # This assumes the synchronous SearchSystem has methods we can adapt
        # In a real implementation, you might need to reimplement parts of SearchSystem

        # Apply filters
        query = base_query
        filter_terms = self._parse_filters(parameters)
        for column, value in filter_terms:
            query = query.where(column == value)

        # Apply search
        search_term = parameters.get("search")
        if search_term:
            search_columns = [self.config.columns[col] for col in self.config.search]
            search_filters = [col.ilike(f"%{search_term}%") for col in search_columns]
            from sqlalchemy import or_

            query = query.where(or_(*search_filters))

        # Apply sorting
        sort_column = parameters.get("sort", self.config.default_sort)
        direction = parameters.get("direction", "asc")
        if sort_column in self.config.columns:
            column = self.config.columns[sort_column]
            if direction == "desc":
                from sqlalchemy import desc

                query = query.order_by(desc(column))
            else:
                query = query.order_by(column)

        # Apply pagination
        limit = parameters.get("limit")
        offset = parameters
