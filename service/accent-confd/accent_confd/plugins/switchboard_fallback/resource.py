# Copyright 2023 Accent Communications

from flask import request

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource

from .schema import SwitchboardFallbackSchema


class SwitchboardFallbackList(ConfdResource):
    schema = SwitchboardFallbackSchema
    has_tenant_uuid = True

    def __init__(self, service, switchboard_dao):
        super().__init__()
        self.service = service
        self.switchboard_dao = switchboard_dao

    @required_acl('confd.switchboards.{switchboard_uuid}.fallbacks.read')
    def get(self, switchboard_uuid):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        switchboard = self.switchboard_dao.get(
            switchboard_uuid, tenant_uuids=tenant_uuids
        )
        return self.schema().dump(switchboard.fallbacks)

    @required_acl('confd.switchboards.{switchboard_uuid}.fallbacks.update')
    def put(self, switchboard_uuid):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        switchboard = self.switchboard_dao.get(
            switchboard_uuid, tenant_uuids=tenant_uuids
        )
        fallbacks = self.schema().load(request.get_json())
        self.service.edit(switchboard, fallbacks)
        return '', 204
