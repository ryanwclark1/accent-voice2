# file: accent_dao/resources/endpoint_sccp/search.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from accent_dao.alchemy.sccpline import SCCPLine
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=SCCPLine,
    columns={
        "id": SCCPLine.id,
        "name": SCCPLine.name,
        "description": SCCPLine.description,
    },
    default_sort="id",
)

sccp_search = SearchSystem(config)
