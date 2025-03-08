# Copyright 2023 Accent Communications

from accent_dao.alchemy.ingress_http import IngressHTTP
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=IngressHTTP,
    columns={'uri': IngressHTTP.uri},
    default_sort='uri',
)

http_ingress_search = SearchSystem(config)
