# file: accent_dao/resources/application/search.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from accent_dao.alchemy.application import Application
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Application,
    columns={
        "uuid": Application.uuid,
        "name": Application.name,
    },
    default_sort="uuid",
)

application_search = SearchSystem(config)
