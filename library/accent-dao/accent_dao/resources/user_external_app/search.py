# Copyright 2025 Accent Communications

from accent_dao.alchemy.user_external_app import UserExternalApp
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=UserExternalApp,
    columns={"name": UserExternalApp.name, "label": UserExternalApp.label},
    search=["name", "label"],
    default_sort="name",
)

user_external_app_search = SearchSystem(config)
