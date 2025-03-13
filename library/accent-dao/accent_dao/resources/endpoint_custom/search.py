# file: accent_dao/resources/endpoint_custom/search.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from accent_dao.alchemy.usercustom import UserCustom
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=UserCustom,
    columns={
        "id": UserCustom.id,
        "interface": UserCustom.interface,
        "context": UserCustom.context,
    },
    default_sort="interface",
)

custom_search = SearchSystem(config)
