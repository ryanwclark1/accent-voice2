# Copyright 2023 Accent Communications

from accent_dao.alchemy.context import Context
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Context,
    columns={
        'id': Context.id,
        'description': Context.description,
        'name': Context.name,
        'label': Context.label,
        'type': Context.type,
    },
    default_sort='id',
)

context_search = SearchSystem(config)
