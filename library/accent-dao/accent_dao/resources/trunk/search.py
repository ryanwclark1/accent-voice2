# file: accent_dao/resources/trunk/search.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from accent_dao.alchemy.trunkfeatures import TrunkFeatures as Trunk
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Trunk,
    columns={
        "id": Trunk.id,
        "context": Trunk.context,
        "description": Trunk.description,
        "name": Trunk.name,
        "label": Trunk.label,
        "outgoing_caller_id_format": Trunk.outgoing_caller_id_format,
    },
    default_sort="id",
    search=["name", "label"],
)


# No changes needed here.
trunk_search = SearchSystem(config)
