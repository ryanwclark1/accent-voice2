# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource


class QueueScheduleItem(ConfdResource):
    has_tenant_uuid = True

    def __init__(self, service, queue_dao, schedule_dao):
        super().__init__()
        self.service = service
        self.queue_dao = queue_dao
        self.schedule_dao = schedule_dao

    @required_acl('confd.queues.{queue_id}.schedules.{schedule_id}.delete')
    def delete(self, queue_id, schedule_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        queue = self.queue_dao.get(queue_id, tenant_uuids=tenant_uuids)
        schedule = self.schedule_dao.get(schedule_id, tenant_uuids=tenant_uuids)
        self.service.dissociate(queue, schedule)
        return '', 204

    @required_acl('confd.queues.{queue_id}.schedules.{schedule_id}.update')
    def put(self, queue_id, schedule_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        queue = self.queue_dao.get(queue_id, tenant_uuids=tenant_uuids)
        schedule = self.schedule_dao.get(schedule_id, tenant_uuids=tenant_uuids)
        self.service.associate(queue, schedule)
        return '', 204
