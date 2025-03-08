# Copyright 2023 Accent Communications

from accent_dao.alchemy.outcall import Outcall
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Outcall,
    columns={
        'id': Outcall.id,
        'description': Outcall.description,
        'name': Outcall.name,
        'preprocess_subroutine': Outcall.preprocess_subroutine,
    },
    default_sort='id',
)

outcall_search = SearchSystem(config)
