# Copyright 2025 Accent Communications

from accent_dao.alchemy.outcall import Outcall
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Outcall,
    columns={
        "id": Outcall.id,
        "name": Outcall.name,
        "description": Outcall.description,
        "preprocess_subroutine": Outcall.preprocess_subroutine,
        "enabled": Outcall.enabled,
        "internal_caller_id": Outcall.internal_caller_id,
        "ring_time": Outcall.ring_time,
    },
    search=["name", "description", "preprocess_subroutine"],
    default_sort="name",
)

outcall_search = SearchSystem(config)
