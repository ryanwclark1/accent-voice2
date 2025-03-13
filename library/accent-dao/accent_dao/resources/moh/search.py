# Copyright 2025 Accent Communications

from accent_dao.alchemy.moh import MOH
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=MOH,
    columns={
        "uuid": MOH.uuid,
        "name": MOH.name,
        "label": MOH.label,
        "mode": MOH.mode,
    },
    default_sort="label",
    search=["name", "label"],
)

moh_search = SearchSystem(config)
