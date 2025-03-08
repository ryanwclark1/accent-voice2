# Copyright 2023 Accent Communications

from accent_dao.alchemy.moh import MOH
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=MOH, columns={'name': MOH.name, 'label': MOH.label}, default_sort='label'
)

moh_search = SearchSystem(config)
