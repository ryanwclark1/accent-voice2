# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource


class IncallScheduleItem(ConfdResource):
    has_tenant_uuid = True

    def __init__(self, service, incall_dao, schedule_dao):
        super().__init__()
        self.service = service
        self.incall_dao = incall_dao
        self.schedule_dao = schedule_dao

    @required_acl('confd.incalls.{incall_id}.schedules.{schedule_id}.delete')
    def delete(self, incall_id, schedule_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        incall = self.incall_dao.get(incall_id, tenant_uuids=tenant_uuids)
        schedule = self.schedule_dao.get(schedule_id, tenant_uuids=tenant_uuids)
        self.service.dissociate(incall, schedule)
        return '', 204

    @required_acl('confd.incalls.{incall_id}.schedules.{schedule_id}.update')
    def put(self, incall_id, schedule_id):
        tenant_uuids = self._build_tenant_list({'recurse': True})
        incall = self.incall_dao.get(incall_id, tenant_uuids=tenant_uuids)
        schedule = self.schedule_dao.get(schedule_id, tenant_uuids=tenant_uuids)
        self.service.associate(incall, schedule)
        return '', 204
