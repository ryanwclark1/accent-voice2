# file: accent_dao/resources/endpoint_iax/search.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from accent_dao.alchemy.useriax import UserIAX
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=UserIAX,
    columns={"name": UserIAX.name, "type": UserIAX.type, "host": UserIAX.host},
    default_sort="name",
)

iax_search = SearchSystem(config)
