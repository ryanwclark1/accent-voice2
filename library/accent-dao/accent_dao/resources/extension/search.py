# file: accent_dao/resources/extension/search.py
# Copyright 2025 Accent Communications

from sqlalchemy import func, select

from accent_dao.alchemy.extension import Extension
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Extension,
    columns={
        "exten": Extension.exten,
        "context": Extension.context,
        "type": Extension.type,
    },
    search=[
        "exten",
    ],
    default_sort="exten",
)


class AsyncSearchSystem(SearchSystem):
    """Extend SearchSystem to add async support."""

    async def search_from_query(self, session, query, parameters=None):
        """Asynchronously perform a search starting from an existing query.

        Args:
            session: SQLAlchemy AsyncSession object.
            query: SQLAlchemy query object.
            parameters: Dictionary of search parameters.

        Returns:
            SearchResult: NamedTuple containing total count and items.

        """
        parameters = self._populate_parameters(parameters)
        self._validate_parameters(parameters)

        query = self._filter(query, parameters["search"])
        query = self._filter_exact_match(query, parameters)

        # Apply sorting
        sort_column_name = parameters["order"]
        sort_direction = parameters["direction"]
        query = self._sort(query, sort_column_name, sort_direction)

        # Apply pagination
        limit = parameters["limit"]
        offset = parameters["offset"]
        query = self._paginate(query, limit, offset)

        # Execute count and fetch queries concurrently using asyncio.gather
        count_query = select(func.count()).select_from(query.subquery())
        count_task = session.execute(count_query)

        # Fetch the rows with the limit and offset using await
        result = await session.execute(query)
        rows = result.scalars().all()

        total = (await count_task).scalar_one()

        return total, rows


extension_search = AsyncSearchSystem(config)
