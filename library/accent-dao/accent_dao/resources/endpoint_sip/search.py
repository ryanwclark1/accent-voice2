# file: accent_dao/resources/endpoint_sip/search.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import func, select

from accent_dao.alchemy.endpoint_sip import EndpointSIP
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=EndpointSIP,
    columns={
        "name": EndpointSIP.name,
        "asterisk_id": EndpointSIP.asterisk_id,
        "label": EndpointSIP.label,
        "template": EndpointSIP.template,
        "caller_id": EndpointSIP.caller_id,
        "username": EndpointSIP.username,
        "password": EndpointSIP.password,
    },
    default_sort="label",
)


class AsyncSearchSystem(SearchSystem):
    """Extend SearchSystem to add async support and handle materialised view."""

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

        # Execute count and fetch queries concurrently using asyncio.gather
        count_query = select(func.count()).select_from(query.subquery())
        count_task = session.execute(count_query)

        # Fetch the rows with the limit and offset using await
        result = await session.execute(query)
        rows = result.scalars().all()

        total = (await count_task).scalar_one()

        return total, rows


sip_search = AsyncSearchSystem(config)
