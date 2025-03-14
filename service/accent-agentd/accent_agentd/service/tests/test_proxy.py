# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from unittest.mock import sentinel as s

from accent_agentd.service.handler.login import LoginHandler
from accent_agentd.service.handler.logoff import LogoffHandler
from accent_agentd.service.handler.membership import MembershipHandler
from accent_agentd.service.handler.on_agent import OnAgentHandler
from accent_agentd.service.handler.on_queue import OnQueueHandler
from accent_agentd.service.handler.pause import PauseHandler
from accent_agentd.service.handler.relog import RelogHandler
from accent_agentd.service.handler.status import StatusHandler
from accent_agentd.service.proxy import ServiceProxy


class TestServiceProxy(unittest.TestCase):
    def setUp(self):
        self.login_handler = Mock(LoginHandler)
        self.logoff_handler = Mock(LogoffHandler)
        self.membership_handler = Mock(MembershipHandler)
        self.on_agent_handler = Mock(OnAgentHandler)
        self.on_queue_handler = Mock(OnQueueHandler)
        self.pause_handler = Mock(PauseHandler)
        self.relog_handler = Mock(RelogHandler)
        self.status_handler = Mock(StatusHandler)
        self.proxy = ServiceProxy()
        self.proxy.login_handler = self.login_handler
        self.proxy.logoff_handler = self.logoff_handler
        self.proxy.membership_handler = self.membership_handler
        self.proxy.on_agent_handler = self.on_agent_handler
        self.proxy.on_queue_handler = self.on_queue_handler
        self.proxy.pause_handler = self.pause_handler
        self.proxy.relog_handler = self.relog_handler
        self.proxy.status_handler = self.status_handler
        self.agent = {'id': s.agent_id}
        self.queue = {'id': s.queue_id}
        self.tenants = ['fake-tenant']

    def test_add_agent_to_queue(self):
        self.proxy.add_agent_to_queue(s.agent_id, s.queue_id, tenant_uuids=self.tenants)
        self.membership_handler.handle_add_to_queue.assert_called_once_with(
            s.agent_id, s.queue_id, tenant_uuids=self.tenants
        )

    def test_remove_agent_from_queue(self):
        self.proxy.remove_agent_from_queue(
            s.agent_id, s.queue_id, tenant_uuids=self.tenants
        )

        self.membership_handler.handle_remove_from_queue.assert_called_once_with(
            s.agent_id, s.queue_id, tenant_uuids=self.tenants
        )

    def test_login_agent_by_id(self):
        self.proxy.login_agent_by_id(
            s.agent_id, s.extension, s.context, tenant_uuids=self.tenants
        )

        self.login_handler.handle_login_by_id.assert_called_once_with(
            s.agent_id, s.extension, s.context, tenant_uuids=self.tenants
        )

    def test_login_agent_by_number(self):
        self.proxy.login_agent_by_number(
            s.agent_number, s.extension, s.context, tenant_uuids=self.tenants
        )

        self.login_handler.handle_login_by_number.assert_called_once_with(
            s.agent_number, s.extension, s.context, tenant_uuids=self.tenants
        )

    def test_login_user_agent(self):
        self.proxy.login_user_agent(s.user_uuid, s.line_id, tenant_uuids=self.tenants)

        self.login_handler.handle_login_user_agent.assert_called_once_with(
            s.user_uuid, s.line_id, tenant_uuids=self.tenants
        )

    def test_logoff_agent_by_id(self):
        self.proxy.logoff_agent_by_id(s.agent_id, tenant_uuids=self.tenants)

        self.logoff_handler.handle_logoff_by_id.assert_called_once_with(
            s.agent_id, tenant_uuids=self.tenants
        )

    def test_logoff_agent_by_number(self):
        self.proxy.logoff_agent_by_number(s.agent_number, tenant_uuids=self.tenants)

        self.logoff_handler.handle_logoff_by_number.assert_called_once_with(
            s.agent_number, tenant_uuids=self.tenants
        )

    def test_logoff_user_agent(self):
        self.proxy.logoff_user_agent(s.user_uuid, tenant_uuids=self.tenants)

        self.logoff_handler.handle_logoff_user_agent.assert_called_once_with(
            s.user_uuid, tenant_uuids=self.tenants
        )

    def test_logoff_all(self):
        self.proxy.logoff_all(tenant_uuids=self.tenants)

        self.logoff_handler.handle_logoff_all.assert_called_once_with(
            tenant_uuids=self.tenants
        )

    def test_relog_all(self):
        self.proxy.relog_all(tenant_uuids=self.tenants)

        self.relog_handler.handle_relog_all.assert_called_once_with(
            tenant_uuids=self.tenants
        )

    def test_pause_agent_by_number(self):
        self.proxy.pause_agent_by_number(
            s.agent_number, s.reason, tenant_uuids=self.tenants
        )

        self.pause_handler.handle_pause_by_number.assert_called_once_with(
            s.agent_number, s.reason, tenant_uuids=self.tenants
        )

    def test_unpause_agent_by_number(self):
        self.proxy.unpause_agent_by_number(s.agent_number, tenant_uuids=self.tenants)

        self.pause_handler.handle_unpause_by_number.assert_called_once_with(
            s.agent_number, tenant_uuids=self.tenants
        )

    def test_get_agent_status_by_id(self):
        self.proxy.get_agent_status_by_id(s.agent_id, tenant_uuids=self.tenants)

        self.status_handler.handle_status_by_id.assert_called_once_with(
            s.agent_id, tenant_uuids=self.tenants
        )

    def test_get_agent_status_by_number(self):
        self.proxy.get_agent_status_by_number(s.agent_number, tenant_uuids=self.tenants)

        self.status_handler.handle_status_by_number.assert_called_once_with(
            s.agent_number, tenant_uuids=self.tenants
        )

    def test_get_agent_statuses(self):
        self.proxy.get_agent_statuses(tenant_uuids=self.tenants)

        self.status_handler.handle_statuses.assert_called_once_with(
            tenant_uuids=self.tenants
        )

    def test_on_agent_updated(self):
        self.proxy.on_agent_updated(self.agent)

        self.on_agent_handler.handle_on_agent_updated.assert_called_once_with(
            self.agent['id']
        )

    def test_on_agent_deleted(self):
        self.proxy.on_agent_deleted(self.agent)

        self.on_agent_handler.handle_on_agent_deleted.assert_called_once_with(
            self.agent['id']
        )

    def test_on_agent_paused(self):
        self.agent['Paused'] = '1'
        self.proxy.on_agent_paused(self.agent)

        self.on_queue_handler.handle_on_agent_paused.assert_called_once_with(self.agent)

    def test_on_agent_unpaused(self):
        self.agent['Paused'] = '0'
        self.proxy.on_agent_paused(self.agent)

        self.on_queue_handler.handle_on_agent_unpaused.assert_called_once_with(
            self.agent
        )

    def test_on_queue_updated(self):
        self.proxy.on_queue_updated(self.queue)

        self.on_queue_handler.handle_on_queue_updated.assert_called_once_with(
            self.queue['id']
        )

    def test_on_queue_deleted(self):
        self.proxy.on_queue_deleted(self.queue)

        self.on_queue_handler.handle_on_queue_deleted.assert_called_once_with(
            self.queue['id']
        )
