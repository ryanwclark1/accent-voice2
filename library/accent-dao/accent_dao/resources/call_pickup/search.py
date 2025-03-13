# Copyright 2025 Accent Communications

from accent_dao.alchemy.pickup import Pickup
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Pickup,
    columns={
        "id": Pickup.id,
        "name": Pickup.name,
        "description": Pickup.description,
        "enabled": Pickup.enabled,
    },
    search=["name", "description"],
    default_sort="name",
)

call_pickup_search = SearchSystem(config)
