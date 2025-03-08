# Copyright 2023 Accent Communications

from accent_dao.alchemy.external_app import ExternalApp
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=ExternalApp,
    columns={'name': ExternalApp.name},
    default_sort='name',
)

external_app_search = SearchSystem(config)
