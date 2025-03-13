# file: accent_dao/resources/user/search.py  # noqa: ERA001
# Copyright 2025 Accent Communications


from sqlalchemy import func, select

from accent_dao.alchemy.userfeatures import UserFeatures as User
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=User,
    columns={
        "id": User.id,
        "uuid": User.uuid,
        "firstname": User.firstname,
        "lastname": User.lastname,
        "fullname": User.fullname,
        "caller_id": User.callerid,
        "description": User.description,
        "userfield": User.userfield,
        "email": User.email,
        "mobile_phone_number": User.mobilephonenumber,
        "music_on_hold": User.musiconhold,
        "outgoing_caller_id": User.outcallerid,
        "preprocess_subroutine": User.preprocess_subroutine,
        "username": User.loginclient,
        "enabled": User.enabled,
        "simultcalls": User.simultcalls,
    },
    search=[
        "fullname",
        "caller_id",
        "description",
        "userfield",
        "email",
        "mobile_phone_number",
        "preprocess_subroutine",
        "outgoing_caller_id",
        "username",
    ],
    default_sort="lastname",
)


class AsyncSearchSystem(SearchSystem):
    """Extend SearchSystem to add async support."""

    async def async_search_from_query(self, session, query, parameters=None):
        """Asynchronously perform a search starting from an existing query."""
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

        # Execute count and fetch queries
        count_query = select(func.count()).select_from(query.subquery())
        count_task = session.execute(count_query)

        result = await session.execute(query)
        rows = result.scalars().all()

        total = (await count_task).scalar_one()
        return SearchResult(total, rows)


user_search = AsyncSearchSystem(config)
