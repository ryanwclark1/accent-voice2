# Copyright 2023 Accent Communications

from accent_dao.alchemy.groupfeatures import GroupFeatures as Group
from accent_dao.resources.utils.search import SearchSystem, SearchConfig


config = SearchConfig(
    table=Group,
    columns={
        'id': Group.id,
        'name': Group.name,
        'label': Group.label,
        'preprocess_subroutine': Group.preprocess_subroutine,
        'exten': Group.exten,
    },
    default_sort='label',
)

group_search = SearchSystem(config)
