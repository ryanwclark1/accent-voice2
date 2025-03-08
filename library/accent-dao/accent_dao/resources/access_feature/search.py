# Copyright 2023 Accent Communications

from accent_dao.alchemy.accessfeatures import AccessFeatures
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=AccessFeatures,
    columns={
        'id': AccessFeatures.id,
        'host': AccessFeatures.host,
        'feature': AccessFeatures.feature,
        'enabled': AccessFeatures.enabled,
    },
    default_sort='host',
)

access_feature_search = SearchSystem(config)
