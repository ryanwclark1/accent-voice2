# Copyright 2023 Accent Communications

from accent_dao.alchemy import QueueMember
from accent_dao.resources.agent import dao as agent_dao
from accent_dao.resources.queue import dao as queue_dao

from .resource import QueueMemberAgentSchema


class QueueMemberMiddleWare:
    def __init__(self, service):
        self._service = service

        self._schema = QueueMemberAgentSchema()

    def _find_or_create_member(self, queue, agent):
        member = self._service.find_member_agent(queue, agent)
        if not member:
            member = QueueMember(agent=agent)
        return member

    def associate(self, body, queue_id, agent_id, tenant_uuids):
        queue = queue_dao.get(queue_id, tenant_uuids=tenant_uuids)
        agent = agent_dao.get(agent_id, tenant_uuids=tenant_uuids)
        member = self._find_or_create_member(queue, agent)
        form = self._schema.load(body)
        member.penalty = form['penalty']
        member.priority = form['priority']
        self._service.associate_member_agent(queue, member)

    def dissociate(self, queue_id, agent_id, tenant_uuids):
        queue = queue_dao.get(queue_id, tenant_uuids=tenant_uuids)
        agent = agent_dao.get(agent_id, tenant_uuids=tenant_uuids)
        member = self._find_or_create_member(queue, agent)
        self._service.dissociate_member_agent(queue, member)
