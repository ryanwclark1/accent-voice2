# Copyright 2023 Accent Communications

from accent_dao.alchemy.useriax import UserIAX
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=UserIAX,
    columns={'name': UserIAX.name, 'type': UserIAX.type, 'host': UserIAX.host},
    default_sort='name',
)

iax_search = SearchSystem(config)
