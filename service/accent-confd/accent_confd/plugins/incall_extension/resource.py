# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource


class IncallExtensionItem(ConfdResource):
    has_tenant_uuid = True

    def __init__(self, middleware):
        super().__init__()
        self._middleware = middleware

    @required_acl('confd.incalls.{incall_id}.extensions.{extension_id}.delete')
    def delete(self, incall_id, extension_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        self._middleware.dissociate(incall_id, extension_id, tenant_uuids)
        return '', 204

    @required_acl('confd.incalls.{incall_id}.extensions.{extension_id}.update')
    def put(self, incall_id, extension_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        self._middleware.associate(incall_id, extension_id, tenant_uuids)
        return '', 204
