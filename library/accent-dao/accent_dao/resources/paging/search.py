# Copyright 2023 Accent Communications

from accent_dao.alchemy.paging import Paging
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Paging,
    columns={
        'id': Paging.id,
        'name': Paging.name,
        'number': Paging.number,
        'announce_sound': Paging.announce_sound,
    },
    default_sort='name',
)

paging_search = SearchSystem(config)
