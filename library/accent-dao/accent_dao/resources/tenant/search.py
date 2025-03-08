# Copyright 2023 Accent Communications

from accent_dao.alchemy.tenant import Tenant
from accent_dao.resources.utils.search import (
    SearchConfig,
    SearchSystem,
)

config = SearchConfig(
    table=Tenant,
    columns={
        'uuid': Tenant.uuid,
    },
    default_sort='uuid',
)

tenant_search = SearchSystem(config)