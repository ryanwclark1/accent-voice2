# Copyright 2023 Accent Communications

from accent_dao.alchemy.extension import Extension
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Extension,
    columns={
        'exten': Extension.exten,
        'context': Extension.context,
        'type': Extension.context_type,
    },
    default_sort='exten',
)


extension_search = SearchSystem(config)
