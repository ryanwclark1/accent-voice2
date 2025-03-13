# Copyright 2025 Accent Communications


from accent_dao.alchemy.meeting_authorization import MeetingAuthorization
from accent_dao.resources.utils.search import SearchConfig, SearchSystem


class MeetingAuthorizationSearchSystem(SearchSystem):
    """Search system for MeetingAuthorization, adds search on meeting_uuid."""

    def search_from_query(self, query, parameters=None):
        if parameters is None:
            parameters = {}
        if meeting_uuid := parameters.pop("meeting_uuid", None):
            query = query.filter(MeetingAuthorization.meeting_uuid == meeting_uuid)
        return super().search_from_query(query, parameters)


config = SearchConfig(
    table=MeetingAuthorization,
    columns={
        "uuid": MeetingAuthorization.uuid,
        "guest_uuid": MeetingAuthorization.guest_uuid,
        "guest_name": MeetingAuthorization.guest_name,
        "status": MeetingAuthorization.status,
        "creation_time": MeetingAuthorization.created_at,
        "meeting_uuid": MeetingAuthorization.meeting_uuid,
    },
    search=["guest_name"],
    default_sort="guest_name",
)

meeting_authorization_search = MeetingAuthorizationSearchSystem(config)
