# Copyright 2023 Accent Communications

from accent_dao.alchemy.meeting_authorization import MeetingAuthorization
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=MeetingAuthorization,
    columns={
        'guest_name': MeetingAuthorization.guest_name,
        'creation_time': MeetingAuthorization.created_at,
    },
    search=['guest_name'],
    default_sort='guest_name',
)

meeting_authorization_search = SearchSystem(config)
