# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource


class OutcallScheduleItem(ConfdResource):
    has_tenant_uuid = True

    def __init__(self, service, outcall_dao, schedule_dao):
        super().__init__()
        self.service = service
        self.outcall_dao = outcall_dao
        self.schedule_dao = schedule_dao

    @required_acl('confd.outcalls.{outcall_id}.schedules.{schedule_id}.delete')
    def delete(self, outcall_id, schedule_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        outcall = self.outcall_dao.get(outcall_id, tenant_uuids=tenant_uuids)
        schedule = self.schedule_dao.get(schedule_id, tenant_uuids=tenant_uuids)
        self.service.dissociate(outcall, schedule)
        return '', 204

    @required_acl('confd.outcalls.{outcall_id}.schedules.{schedule_id}.update')
    def put(self, outcall_id, schedule_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        outcall = self.outcall_dao.get(outcall_id, tenant_uuids=tenant_uuids)
        schedule = self.schedule_dao.get(schedule_id, tenant_uuids=tenant_uuids)
        self.service.associate(outcall, schedule)
        return '', 204
