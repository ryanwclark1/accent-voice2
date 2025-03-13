# Copyright 2025 Accent Communications

from sqlalchemy import func, select

from accent_dao.alchemy.meeting import Meeting
from accent_dao.alchemy.meeting_authorization import MeetingAuthorization
from accent_dao.resources.utils.search import SearchConfig, SearchSystem


class MeetingSearchSystem(SearchSystem):
    """Custom search system for Meeting."""

    def search_from_query(self, query, parameters=None):
        """Perform search, apply filters, sorting, and pagination."""
        if parameters is None:
            parameters = {}
        if owner := parameters.pop("owner", None):
            query = self._filter_owner(query, owner)
        if created_before := parameters.pop("created_before", None):
            query = self._filter_created_before(query, created_before)
        return super().search_from_query(query, parameters)

    def _filter_owner(self, query, owner):
        return query.filter(
            Meeting.uuid.in_(
                select(MeetingAuthorization.meeting_uuid).where(
                    MeetingAuthorization.guest_uuid == owner
                )
            )
        )

    def _filter_created_before(self, query, before):
        return query.filter(Meeting.created_at < before)


config = SearchConfig(
    table=Meeting,
    columns={
        "uuid": Meeting.uuid,
        "name": Meeting.name,
        "persistent": Meeting.persistent,
        "require_authorization": Meeting.require_authorization,
        "created_at": Meeting.created_at,
        "number": Meeting.number,
    },
    search=["name"],
    default_sort="name",
)

meeting_search = MeetingSearchSystem(config)
