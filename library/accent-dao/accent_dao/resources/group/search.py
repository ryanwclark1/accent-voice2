# Copyright 2025 Accent Communications

from sqlalchemy import select

from accent_dao.alchemy.groupfeatures import GroupFeatures
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=GroupFeatures,
    columns={
        "id": GroupFeatures.id,
        "name": GroupFeatures.name,
        "label": GroupFeatures.label,
        "preprocess_subroutine": GroupFeatures.preprocess_subroutine,
        "exten": GroupFeatures.exten,
    },
    default_sort="label",
)

group_search = SearchSystem(config)
