# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource


class QueueExtensionItem(ConfdResource):
    has_tenant_uuid = True

    def __init__(self, service, queue_dao, extension_dao):
        super().__init__()
        self.service = service
        self.queue_dao = queue_dao
        self.extension_dao = extension_dao

    @required_acl('confd.queues.{queue_id}.extensions.{extension_id}.delete')
    def delete(self, queue_id, extension_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})

        queue = self.queue_dao.get(queue_id, tenant_uuids=tenant_uuids)
        extension = self.extension_dao.get(extension_id, tenant_uuids=tenant_uuids)

        self.service.dissociate(queue, extension)
        return '', 204

    @required_acl('confd.queues.{queue_id}.extensions.{extension_id}.update')
    def put(self, queue_id, extension_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})

        queue = self.queue_dao.get(queue_id, tenant_uuids=tenant_uuids)
        extension = self.extension_dao.get(extension_id, tenant_uuids=tenant_uuids)

        self.service.associate(queue, extension)
        return '', 204
