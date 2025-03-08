# Copyright 2023 Accent Communications

from accent_dao.alchemy.user_external_app import UserExternalApp
from accent_dao.resources.utils.search import SearchSystem
from accent_dao.resources.utils.search import SearchConfig


config = SearchConfig(
    table=UserExternalApp,
    columns={'name': UserExternalApp.name},
    default_sort='name',
)

user_external_app_search = SearchSystem(config)
