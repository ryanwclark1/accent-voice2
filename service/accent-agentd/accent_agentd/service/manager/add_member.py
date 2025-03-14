# Copyright 2023 Accent Communications

from accent_dao.helpers import db_utils

from accent_agentd.exception import AgentAlreadyInQueueError, QueueDifferentTenantError


class AddMemberManager:
    def __init__(
        self, add_to_queue_action, amid_client, agent_status_dao, queue_member_dao
    ):
        self._add_to_queue_action = add_to_queue_action
        self._amid_client = amid_client
        self._agent_status_dao = agent_status_dao
        self._queue_member_dao = queue_member_dao

    def add_agent_to_queue(self, agent, queue):
        self._check_agent_in_same_tenant_queue(agent, queue)
        self._check_agent_is_not_member_of_queue(agent, queue)
        self._add_queue_member(agent, queue)
        self._send_agent_added_event(agent, queue)
        self._add_to_queue_if_logged(agent, queue)

    def _check_agent_in_same_tenant_queue(self, agent, queue):
        if agent.tenant_uuid != queue.tenant_uuid:
            raise QueueDifferentTenantError()

    def _check_agent_is_not_member_of_queue(self, agent, queue):
        for agent_queue in agent.queues:
            if agent_queue.name == queue.name:
                raise AgentAlreadyInQueueError()

    def _add_queue_member(self, agent, queue):
        with db_utils.session_scope():
            self._queue_member_dao.add_agent_to_queue(
                agent.id, agent.number, queue.name
            )

    def _send_agent_added_event(self, agent, queue):
        self._amid_client.action(
            'UserEvent',
            {
                'UserEvent': 'AgentAddedToQueue',
                'AgentID': agent.id,
                'AgentNumber': agent.number,
                'QueueName': queue.name,
            },
        )

    def _add_to_queue_if_logged(self, agent, queue):
        with db_utils.session_scope():
            agent_status = self._agent_status_dao.get_status(agent.id)
        if agent_status is not None:
            self._add_to_queue_action.add_agent_to_queue(agent_status, queue)
