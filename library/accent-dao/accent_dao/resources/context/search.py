# file: accent_dao/resources/context/search.py
# Copyright 2025 Accent Communications

from accent_dao.alchemy.context import Context
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Context,
    columns={
        "id": Context.id,
        "description": Context.description,
        "name": Context.name,
        "label": Context.label,
        "type": Context.contexttype,
    },
    default_sort="id",
)

context_search = SearchSystem(config)
