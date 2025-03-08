# Copyright 2023 Accent Communications

from .resource import ConfBridgeAccentDefaultBridgeList, ConfBridgeAccentDefaultUserList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            ConfBridgeAccentDefaultBridgeList,
            '/asterisk/confbridge/accent_default_bridge',
            resource_class_args=(service,),
        )

        api.add_resource(
            ConfBridgeAccentDefaultUserList,
            '/asterisk/confbridge/accent_default_user',
            resource_class_args=(service,),
        )
