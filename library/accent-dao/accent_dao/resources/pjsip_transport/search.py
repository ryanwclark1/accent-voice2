# Copyright 2023 Accent Communications

from accent_dao.alchemy.pjsip_transport import PJSIPTransport
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=PJSIPTransport,
    columns={
        'uuid': PJSIPTransport.uuid,
        'name': PJSIPTransport.name,
    },
    search={'name': PJSIPTransport.name},
    default_sort='name',
)
transport_search = SearchSystem(config)
