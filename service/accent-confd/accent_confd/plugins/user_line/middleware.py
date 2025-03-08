# Copyright 2023 Accent Communications

from accent_dao.resources.line import dao as line_dao
from accent_dao.resources.user import dao as user_dao


class UserLineAssociationMiddleWare:
    def __init__(self, service):
        self._service = service

    def associate(self, user_id, line_id, tenant_uuids):
        user = user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        line = line_dao.get(line_id, tenant_uuids=tenant_uuids)
        self._service.associate(user, line)

    def dissociate(self, user_id, line_id, tenant_uuids):
        user = user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        line = line_dao.get(line_id, tenant_uuids=tenant_uuids)
        self._service.dissociate(user, line)

    def dissociate_all_lines(self, user_id, tenant_uuids):
        user = user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        for line in user.lines:
            self._service.dissociate(user, line)
