# Copyright 2023 Accent Communications

from accent_dao.alchemy.rightcall import RightCall as CallPermission
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=CallPermission,
    columns={
        'id': CallPermission.id,
        'name': CallPermission.name,
        'description': CallPermission.description,
        'enabled': CallPermission.enabled,
        'mode': CallPermission.mode,
    },
    default_sort='name',
)

call_permission_search = SearchSystem(config)
