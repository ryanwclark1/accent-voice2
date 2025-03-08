# Copyright 2023 Accent Communications

from accent_dao.alchemy.staticiax import StaticIAX as RegisterIAX
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=RegisterIAX, columns={'id': RegisterIAX.id}, default_sort='id'
)


class RegisterIAXSearchSystem(SearchSystem):
    def search(self, session, parameters=None):
        query = session.query(self.config.table).filter(
            RegisterIAX.var_name == 'register'
        )
        return self.search_from_query(query, parameters)


register_iax_search = RegisterIAXSearchSystem(config)
