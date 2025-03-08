# Copyright 2023 Accent Communications

from accent_dao.resources.agent import dao as agent_dao
from accent_dao.resources.user import dao as user_dao


class UserAgentAssociationMiddleWare:
    def __init__(self, service):
        self._service = service

    def associate(self, user_id, agent_id, tenant_uuids):
        user = user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        agent = agent_dao.get(agent_id, tenant_uuids=tenant_uuids)
        self._service.associate(user, agent)

    def dissociate(self, user_id, tenant_uuids):
        user = user_dao.get_by_id_uuid(user_id, tenant_uuids=tenant_uuids)
        self._service.dissociate(user)
