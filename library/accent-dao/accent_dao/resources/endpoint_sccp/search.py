# Copyright 2023 Accent Communications

from accent_dao.alchemy.sccpline import SCCPLine
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(table=SCCPLine, columns={'id': SCCPLine.id}, default_sort='id')

sccp_search = SearchSystem(config)
