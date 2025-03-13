# Copyright 2025 Accent Communications

from sqlalchemy import and_

from accent_dao.alchemy.staticiax import StaticIAX as RegisterIAX
from accent_dao.resources.utils.search import SearchConfig, SearchSystem


class RegisterIAXSearchSystem(SearchSystem):
    """Search system for RegisterIAX, to find only register type."""

    def search_from_query(self, query, parameters=None):
        """Perform search for register entries with var_name filter."""
        query = query.filter(RegisterIAX.var_name == "register")
        return super().search_from_query(query, parameters)


config = SearchConfig(
    table=RegisterIAX,
    columns={"id": RegisterIAX.id},
    default_sort="id",
)

register_iax_search = RegisterIAXSearchSystem(config)
