# Copyright 2023 Accent Communications

from .resource import HEPGeneralList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            HEPGeneralList, '/asterisk/hep/general', resource_class_args=(service,)
        )
