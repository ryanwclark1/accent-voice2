# Copyright 2023 Accent Communications

from accent_dao.alchemy.pickup import Pickup as CallPickup
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=CallPickup,
    columns={
        'id': CallPickup.id,
        'name': CallPickup.name,
        'description': CallPickup.description,
        'enabled': CallPickup.enabled,
    },
    search=['name', 'description'],
    default_sort='name',
)

call_pickup_search = SearchSystem(config)
