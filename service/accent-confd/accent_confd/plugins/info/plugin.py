# Copyright 2023 Accent Communications

from .resource import Info
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(Info, '/infos', resource_class_args=(service,))
