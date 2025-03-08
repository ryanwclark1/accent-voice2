# Copyright 2023 Accent Communications

from accent_dao.alchemy.meeting import Meeting
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Meeting,
    columns={
        'name': Meeting.name,
        'persistent': Meeting.persistent,
        'require_authorization': Meeting.require_authorization,
        'creation_time': Meeting.created_at,
    },
    search=['name'],
    default_sort='name',
)

meeting_search = SearchSystem(config)
