# Copyright 2023 Accent Communications

from flask import request

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource

from .schema import QueueFallbackSchema


class QueueFallbackList(ConfdResource):
    schema = QueueFallbackSchema
    has_tenant_uuid = True

    def __init__(self, service, queue_dao):
        super().__init__()
        self.service = service
        self.queue_dao = queue_dao

    @required_acl('confd.queues.{queue_id}.fallbacks.read')
    def get(self, queue_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        queue = self.queue_dao.get(queue_id, tenant_uuids=tenant_uuids)
        return self.schema().dump(queue.fallbacks)

    @required_acl('confd.queues.{queue_id}.fallbacks.update')
    def put(self, queue_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        queue = self.queue_dao.get(queue_id, tenant_uuids=tenant_uuids)
        fallbacks = self.schema().load(request.get_json())
        self.service.edit(queue, fallbacks)
        return '', 204
