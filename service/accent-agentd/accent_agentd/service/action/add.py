# Copyright 2023 Accent Communications

import logging

from accent_dao.helpers import db_utils

from accent_agentd.service.helper import format_agent_member_name, format_agent_skills

logger = logging.getLogger(__name__)


class AddToQueueAction:
    def __init__(self, amid_client, agent_status_dao):
        self._amid_client = amid_client
        self._agent_status_dao = agent_status_dao

    def add_agent_to_queue(self, agent_status, queue):
        self._update_asterisk(agent_status, queue)
        self._update_agent_status(agent_status, queue)

    def _update_asterisk(self, agent_status, queue):
        member_name = format_agent_member_name(agent_status.agent_number)
        skills = format_agent_skills(agent_status.agent_id)
        response = self._amid_client.action(
            'QueueAdd',
            {
                'Queue': queue.name,
                'Interface': agent_status.interface,
                'MemberName': member_name,
                'StateInterface': agent_status.state_interface,
                'Penalty': queue.penalty,
                'Skills': skills,
            },
        )
        if response[0]['Response'] != 'Success':
            logger.warning(
                'Failure to add interface %r to queue %r',
                agent_status.interface,
                queue.name,
            )

    def _update_agent_status(self, agent_status, queue):
        with db_utils.session_scope():
            self._agent_status_dao.add_agent_to_queues(agent_status.agent_id, [queue])
