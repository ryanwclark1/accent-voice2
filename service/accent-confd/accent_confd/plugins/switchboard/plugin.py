# Copyright 2023 Accent Communications

from accent_dao.resources.moh import dao as moh_dao

from .resource import SwitchboardItem, SwitchboardList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            SwitchboardList, '/switchboards', resource_class_args=(service, moh_dao)
        )

        api.add_resource(
            SwitchboardItem,
            '/switchboards/<uuid>',
            endpoint='switchboards',
            resource_class_args=(service, moh_dao),
        )
