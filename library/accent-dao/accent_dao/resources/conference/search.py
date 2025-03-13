# file: accent_dao/resources/conference/search.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from accent_dao.alchemy.conference import Conference
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Conference,
    columns={
        "id": Conference.id,
        "name": Conference.name,
        "preprocess_subroutine": Conference.preprocess_subroutine,
        "exten": Conference.exten,
    },
    default_sort="name",
)

conference_search = SearchSystem(config)
