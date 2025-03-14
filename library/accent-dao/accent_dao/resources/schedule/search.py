# Copyright 2025 Accent Communications

from accent_dao.alchemy.schedule import Schedule
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Schedule,
    columns={
        "id": Schedule.id,
        "name": Schedule.name,
        "timezone": Schedule.timezone,
    },
    search=["name", "timezone"],
    default_sort="name",
)

schedule_search = SearchSystem(config)
