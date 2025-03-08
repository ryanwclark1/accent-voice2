# Copyright 2023 Accent Communications

from .resource import IAXCallNumberLimitsList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            IAXCallNumberLimitsList,
            '/asterisk/iax/callnumberlimits',
            resource_class_args=(service,),
        )
