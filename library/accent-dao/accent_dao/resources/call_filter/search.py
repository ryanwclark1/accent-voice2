# file: accent_dao/resources/call_filter/search.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from accent_dao.alchemy.callfilter import Callfilter
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Callfilter,
    columns={
        "id": Callfilter.id,
        "name": Callfilter.name,
        "description": Callfilter.description,
        "enabled": Callfilter.enabled,
    },
    default_sort="name",
)

call_filter_search = SearchSystem(config)
