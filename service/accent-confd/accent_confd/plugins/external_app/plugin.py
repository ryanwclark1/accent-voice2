# Copyright 2023 Accent Communications

from .resource import ExternalAppItem, ExternalAppList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            ExternalAppList,
            '/external/apps',
            resource_class_args=(service,),
        )

        api.add_resource(
            ExternalAppItem,
            '/external/apps/<name>',
            endpoint='external_apps',
            resource_class_args=(service,),
        )
