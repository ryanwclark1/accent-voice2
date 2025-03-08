# Copyright 2023 Accent Communications

from accent_dao.alchemy.feature_extension import FeatureExtension
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=FeatureExtension,
    columns={'exten': FeatureExtension.exten, 'feature': FeatureExtension.feature},
    default_sort='exten',
)


feature_extension_search = SearchSystem(config)
