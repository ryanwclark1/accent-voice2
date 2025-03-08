# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource


class GroupExtensionItem(ConfdResource):
    has_tenant_uuid = True

    def __init__(self, service, group_dao, extension_dao):
        super().__init__()
        self.service = service
        self.group_dao = group_dao
        self.extension_dao = extension_dao

    @required_acl('confd.groups.{group_uuid}.extensions.{extension_id}.delete')
    def delete(self, group_uuid, extension_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})

        group = self.group_dao.get(group_uuid, tenant_uuids=tenant_uuids)
        extension = self.extension_dao.get(extension_id, tenant_uuids=tenant_uuids)

        self.service.dissociate(group, extension)
        return '', 204

    @required_acl('confd.groups.{group_uuid}.extensions.{extension_id}.update')
    def put(self, group_uuid, extension_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})

        group = self.group_dao.get(group_uuid, tenant_uuids=tenant_uuids)
        extension = self.extension_dao.get(extension_id, tenant_uuids=tenant_uuids)

        self.service.associate(group, extension)
        return '', 204
