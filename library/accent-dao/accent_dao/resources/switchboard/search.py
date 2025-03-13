# file: accent_dao/resources/switchboard/search.py
# Copyright 2025 Accent Communications

from sqlalchemy import and_, func
from sqlalchemy.sql.expression import cast, select
from sqlalchemy.sql.sqltypes import String

from accent_dao.alchemy.dialaction import Dialaction
from accent_dao.alchemy.incall import Incall
from accent_dao.alchemy.switchboard import Switchboard
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Switchboard,
    columns={
        "name": Switchboard.name,
        "exten": Incall.exten,
    },
    search=[
        "name",
        "exten",
    ],
    default_sort="name",
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

    def _search_on_extension(self, query):
        return (
            query.outerjoin(
                Dialaction,
                and_(
                    Dialaction.action == "switchboard",
                    Dialaction.actionarg1 == Switchboard.uuid,
                ),
            )
            .outerjoin(
                Incall,
                and_(
                    Dialaction.category == "incall",
                    Dialaction.categoryval == cast(Incall.id, String),
                    Incall.commented == 0,
                ),
            )
            .group_by(Switchboard)
        )


switchboard_search = AsyncSearchSystem(config)
