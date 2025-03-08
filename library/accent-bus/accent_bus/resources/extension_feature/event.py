# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent
from ..common.types import UUIDStr


class ExtensionFeatureEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'extension_feature_edited'
    routing_key_fmt = 'config.extension_feature.edited'

    def __init__(self, feature_extension_uuid: UUIDStr):
        content = {'uuid': feature_extension_uuid}
        super().__init__(content)
