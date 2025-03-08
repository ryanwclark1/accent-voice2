# Copyright 2023 Accent Communications

from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.resources.utils.search import SearchSystem, SearchConfig


config = SearchConfig(
    table=QueueFeatures,
    columns={
        'id': QueueFeatures.id,
        'name': QueueFeatures.name,
        'label': QueueFeatures.label,
        'preprocess_subroutine': QueueFeatures.preprocess_subroutine,
        'exten': QueueFeatures.exten,
    },
    default_sort='id',
)

queue_search = SearchSystem(config)
