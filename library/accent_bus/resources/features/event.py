# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class FeaturesApplicationmapEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'features_applicationmap_edited'
    routing_key_fmt = 'config.features_applicationmap.edited'

    def __init__(self) -> None:
        super().__init__()


class FeaturesFeaturemapEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'features_featuremap_edited'
    routing_key_fmt = 'config.features_featuremap.edited'

    def __init__(self) -> None:
        super().__init__()


class FeaturesGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'features_general_edited'
    routing_key_fmt = 'config.features_general.edited'

    def __init__(self) -> None:
        super().__init__()
