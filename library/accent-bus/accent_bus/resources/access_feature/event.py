# Copyright 2023 Accent Communications

from __future__ import annotations

from ..common.event import ServiceEvent
from .types import AccessFeatureDict


class AccessFeatureCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'access_feature_created'
    routing_key_fmt = 'config.access_feature.created'

    def __init__(self, access_feature_info: AccessFeatureDict):
        super().__init__(content=access_feature_info)


class AccessFeatureDeletedEvent(ServiceEvent):
    service = 'confd'
    name = 'access_feature_deleted'
    routing_key_fmt = 'config.access_feature.deleted'

    def __init__(self, access_feature_info: AccessFeatureDict):
        super().__init__(content=access_feature_info)


class AccessFeatureEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'access_feature_edited'
    routing_key_fmt = 'config.access_feature.edited'

    def __init__(self, access_feature_info: AccessFeatureDict):
        super().__init__(content=access_feature_info)
