# Copyright 2023 Accent Communications

from .resource import CallPermissionItem, CallPermissionList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            CallPermissionList, '/callpermissions', resource_class_args=(service,)
        )

        api.add_resource(
            CallPermissionItem,
            '/callpermissions/<int:id>',
            endpoint='callpermissions',
            resource_class_args=(service,),
        )
