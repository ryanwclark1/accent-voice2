# Copyright 2023 Accent Communications

from accent_dao.resources.func_key_template import dao as template_dao
from accent_dao.resources.user import dao as user_dao


class UserFuncKeyTemplateAssociationMiddleWare:
    def __init__(self, service):
        self._service = service

    def associate(self, user_id, template_id, tenant_uuids):
        user = user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        template = template_dao.get(template_id, tenant_uuids=tenant_uuids)
        self._service.associate(user, template)

    def dissociate(self, user_id, template_id, tenant_uuids):
        user = user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        template = template_dao.get(template_id, tenant_uuids=tenant_uuids)
        self._service.dissociate(user, template)
