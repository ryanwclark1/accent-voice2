# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock

from accent_agentd.service.handler.relog import RelogHandler
from accent_agentd.service.manager.relog import RelogManager


class TestRelogHandler(unittest.TestCase):
    def setUp(self):
        self.relog_manager = Mock(RelogManager)
        self.agent_status_dao = Mock()
        self.relog_handler = RelogHandler(self.relog_manager)
        self.tenants = ['fake-tenant']

    def test_handle_relog_all(self):
        self.relog_handler.handle_relog_all(tenant_uuids=self.tenants)

        self.relog_manager.relog_all_agents.assert_called_once_with(
            tenant_uuids=self.tenants
        )
