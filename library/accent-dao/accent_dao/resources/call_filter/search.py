# Copyright 2023 Accent Communications

from accent_dao.alchemy.callfilter import Callfilter as CallFilter
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=CallFilter,
    columns={
        'id': CallFilter.id,
        'name': CallFilter.name,
        'description': CallFilter.description,
    },
    default_sort='name',
)

call_filter_search = SearchSystem(config)
