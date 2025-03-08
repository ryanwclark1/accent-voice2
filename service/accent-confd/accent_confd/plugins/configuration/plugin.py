# Copyright 2023 Accent Communications

from .resource import LiveReloadResource
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            LiveReloadResource,
            '/configuration/live_reload',
            resource_class_args=(service,),
        )
