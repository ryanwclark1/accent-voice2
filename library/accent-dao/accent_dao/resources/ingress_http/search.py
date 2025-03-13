# Copyright 2025 Accent Communications

from sqlalchemy import Text

from accent_dao.alchemy.ingress_http import IngressHTTP
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=IngressHTTP,
    columns={"uri": IngressHTTP.uri, "tenant_uuid": IngressHTTP.tenant_uuid},
    default_sort="uri",
    search=["uri"],  # Added search capabilities on the 'uri' field.
)

http_ingress_search = SearchSystem(config)
