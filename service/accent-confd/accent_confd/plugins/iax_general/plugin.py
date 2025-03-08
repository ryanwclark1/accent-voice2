# Copyright 2023 Accent Communications

from .resource import IAXGeneralList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            IAXGeneralList, '/asterisk/iax/general', resource_class_args=(service,)
        )
