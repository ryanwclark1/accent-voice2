# Copyright 2025 Accent Communications

from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=QueueFeatures,
    columns={
        "id": QueueFeatures.id,
        "name": QueueFeatures.name,
        "label": QueueFeatures.label,
        "preprocess_subroutine": QueueFeatures.preprocess_subroutine,
        "exten": QueueFeatures.exten,
    },
    search=["name", "label", "exten"],
    default_sort="name",
)

queue_search = SearchSystem(config)
