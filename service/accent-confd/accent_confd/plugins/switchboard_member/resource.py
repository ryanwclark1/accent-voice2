# Copyright 2023 Accent Communications

from flask import request

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource


class SwitchboardMemberUserItem(ConfdResource):
    has_tenant_uuid = True

    def __init__(self, middleware):
        super().__init__()
        self._middleware = middleware

    @required_acl('confd.switchboards.{switchboard_uuid}.members.users.update')
    def put(self, switchboard_uuid):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        self._middleware.associate(request.get_json(), switchboard_uuid, tenant_uuids)
        return '', 204
