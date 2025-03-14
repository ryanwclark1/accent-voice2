# Copyright 2023 Accent Communications

import datetime
import unittest
from unittest.mock import ANY, Mock, call

from accent_amid_client.exceptions import AmidProtocolError
from accent_bus.resources.agent.event import AgentStatusUpdatedEvent
from hamcrest import assert_that, contains_inanyorder, has_entries

from accent_agentd.service.action.logoff import LogoffAction


class TestLogoffAction(unittest.TestCase):
    def setUp(self):
        self.amid_client = Mock()
        self.queue_log_manager = Mock()
        self.blf_manager = Mock()
        self.pause_manager = Mock()
        self.agent_status_dao = Mock()
        self.user_dao = Mock()
        self.agent_dao = Mock()
        self.bus_publisher = Mock()
        self.logoff_action = LogoffAction(
            self.amid_client,
            self.queue_log_manager,
            self.blf_manager,
            self.pause_manager,
            self.agent_status_dao,
            self.user_dao,
            self.agent_dao,
            self.bus_publisher,
        )

    def test_logoff_agent(self):
        agent_id = 10
        user_id = 42
        agent_number = '10'
        queue_name = 'q1'
        queue = Mock()
        queue.name = queue_name
        agent_status = Mock(user_ids=[user_id])
        agent_status.agent_id = agent_id
        agent_status.agent_number = agent_number
        agent_status.login_at = datetime.datetime.utcnow()
        agent_status.queues = [queue]
        tenant_uuid = '00000000-0000-4000-8000-000000001ebc'
        self.user_dao.find_all_by_agent_id.return_value = [
            Mock(uuid='42'),
            Mock(uuid='43'),
        ]
        self.agent_dao.agent_with_id.return_value = Mock(tenant_uuid=tenant_uuid)
        event = AgentStatusUpdatedEvent(10, 'logged_out', tenant_uuid, ['42', '43'])
        self.pause_manager.unpause_agent.side_effect = AmidProtocolError(
            Mock(json=Mock(return_value=[{'Message': 'Interface not found'}]))
        )

        self.logoff_action.logoff_agent(agent_status)

        self.amid_client.action.assert_called_once_with(
            'QueueRemove', {'Queue': queue.name, 'Interface': agent_status.interface}
        )
        assert_that(
            self.blf_manager.set_user_blf.call_args_list,
            contains_inanyorder(
                call(user_id, 'agentstaticlogin', 'NOT_INUSE', f'*{agent_id}'),
                call(user_id, 'agentstaticlogin', 'NOT_INUSE', agent_number),
                call(user_id, 'agentstaticlogoff', 'INUSE', f'*{agent_id}'),
                call(user_id, 'agentstaticlogoff', 'INUSE', agent_number),
                call(user_id, 'agentstaticlogtoggle', 'NOT_INUSE', f'*{agent_id}'),
                call(user_id, 'agentstaticlogtoggle', 'NOT_INUSE', agent_number),
            ),
        )
        self.pause_manager.unpause_agent.assert_called_once_with(agent_status)
        self.queue_log_manager.on_agent_logged_off.assert_called_once_with(
            agent_number, agent_status.extension, agent_status.context, ANY
        )
        self.agent_status_dao.remove_agent_from_all_queues.assert_called_once_with(
            agent_id
        )
        self.agent_status_dao.log_off_agent.assert_called_once_with(agent_id)

        assert_that(
            event.headers,
            has_entries(
                {
                    'tenant_uuid': tenant_uuid,
                    'user_uuid:42': True,
                    'user_uuid:43': True,
                }
            ),
        )
        self.bus_publisher.publish.assert_called_once_with(event)

    def test_logoff_agent_agent_not_paused(self):
        agent_id = 10
        user_id = 42
        agent_number = '10'
        queue_name = 'q1'
        queue = Mock()
        queue.name = queue_name
        agent_status = Mock(user_ids=[user_id])
        agent_status.agent_id = agent_id
        agent_status.agent_number = agent_number
        agent_status.login_at = datetime.datetime.utcnow()
        agent_status.queues = [queue]
        tenant_uuid = '00000000-0000-4000-8000-000000001ebc'
        self.user_dao.find_all_by_agent_id.return_value = [
            Mock(uuid='42'),
            Mock(uuid='43'),
        ]
        self.agent_dao.agent_with_id.return_value = Mock(tenant_uuid=tenant_uuid)
        event = AgentStatusUpdatedEvent(10, 'logged_out', tenant_uuid, ['42', '43'])

        self.logoff_action.logoff_agent(agent_status)

        self.amid_client.action.assert_called_once_with(
            'QueueRemove', {'Queue': queue.name, 'Interface': agent_status.interface}
        )
        assert_that(
            self.blf_manager.set_user_blf.call_args_list,
            contains_inanyorder(
                call(user_id, 'agentstaticlogin', 'NOT_INUSE', f'*{agent_id}'),
                call(user_id, 'agentstaticlogin', 'NOT_INUSE', agent_number),
                call(user_id, 'agentstaticlogoff', 'INUSE', f'*{agent_id}'),
                call(user_id, 'agentstaticlogoff', 'INUSE', agent_number),
                call(user_id, 'agentstaticlogtoggle', 'NOT_INUSE', f'*{agent_id}'),
                call(user_id, 'agentstaticlogtoggle', 'NOT_INUSE', agent_number),
            ),
        )
        self.pause_manager.unpause_agent.assert_called_once_with(agent_status)
        self.queue_log_manager.on_agent_logged_off.assert_called_once_with(
            agent_number, agent_status.extension, agent_status.context, ANY
        )
        self.agent_status_dao.remove_agent_from_all_queues.assert_called_once_with(
            agent_id
        )
        self.agent_status_dao.log_off_agent.assert_called_once_with(agent_id)

        assert_that(
            event.headers,
            has_entries(
                {
                    'tenant_uuid': tenant_uuid,
                    'user_uuid:42': True,
                    'user_uuid:43': True,
                }
            ),
        )
        self.bus_publisher.publish.assert_called_once_with(event)

    def test_logoff_agent_already_off_on_asterisk(self):
        agent_id = 10
        agent_number = '10'
        queue_name = 'q1'
        queue = Mock()
        queue.name = queue_name
        agent_status = Mock(user_ids=[])
        agent_status.agent_id = agent_id
        agent_status.agent_number = agent_number
        agent_status.login_at = datetime.datetime.utcnow()
        agent_status.queues = [queue]
        self.user_dao.find_all_by_agent_id.return_value = [
            Mock(uuid='42'),
            Mock(uuid='43'),
        ]
        tenant_uuid = '00000000-0000-4000-8000-000000001ebc'
        self.agent_dao.agent_with_id.return_value = Mock(tenant_uuid=tenant_uuid)
        event = AgentStatusUpdatedEvent(10, 'logged_out', tenant_uuid, ['42', '43'])

        response = Mock()
        response.json.return_value = [
            {'Message': 'Unable to remove interface: Not there'}
        ]
        self.amid_client.action.side_effect = AmidProtocolError(response)

        self.logoff_action.logoff_agent(agent_status)

        self.amid_client.action.assert_called_once_with(
            'QueueRemove', {'Queue': queue.name, 'Interface': agent_status.interface}
        )
        self.queue_log_manager.on_agent_logged_off.assert_called_once_with(
            agent_number, agent_status.extension, agent_status.context, ANY
        )
        self.agent_status_dao.remove_agent_from_all_queues.assert_called_once_with(
            agent_id
        )
        self.agent_status_dao.log_off_agent.assert_called_once_with(agent_id)

        assert_that(
            event.headers,
            has_entries(
                {
                    'tenant_uuid': tenant_uuid,
                    'user_uuid:42': True,
                    'user_uuid:43': True,
                }
            ),
        )
        self.bus_publisher.publish.assert_called_once_with(event)
