# Copyright 2023 Accent Communications

from .middleware import SwitchboardMemberMiddleWare
from .resource import SwitchboardMemberUserItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        middleware_handle = dependencies['middleware_handle']
        service = build_service()
        switchboard_member_middleware = SwitchboardMemberMiddleWare(service)
        middleware_handle.register('switchboard_member', switchboard_member_middleware)

        api.add_resource(
            SwitchboardMemberUserItem,
            '/switchboards/<uuid:switchboard_uuid>/members/users',
            endpoint='switchboard_member_users',
            resource_class_args=(switchboard_member_middleware,),
        )
