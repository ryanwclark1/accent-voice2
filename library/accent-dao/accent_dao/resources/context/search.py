# Copyright 2025 Accent Communications

from accent_dao.alchemy.context import Context
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Context,
    columns={
        "id": Context.id,
        "name": Context.name,
        "label": Context.label,
        "description": Context.description,
        "type": Context.type,
        "enabled": Context.enabled,
    },
    search=["name", "description", "label"],
    default_sort="id",
)

context_search = SearchSystem(config)
