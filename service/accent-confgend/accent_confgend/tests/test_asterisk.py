# Copyright 2023 Accent Communications


import unittest
from unittest.mock import Mock, patch

from accent_confgend.asterisk import AsteriskFrontend
from accent_confgend.generators.tests.util import assert_config_equal


class Test(unittest.TestCase):
    def setUp(self):
        self._config = {
            'templates': {'contextsconf': None},
        }
        self.tpl_helper = Mock()
        self.asteriskFrontEnd = AsteriskFrontend(self._config, self.tpl_helper)

    @patch('accent_dao.asterisk_conf_dao.find_agent_queue_skills_settings')
    def test_queueskills_conf(self, find_agent_queue_skills_settings):
        find_agent_queue_skills_settings.return_value = [
            {'id': 1, 'name': 'test-skill', 'weight': 10},
        ]
        assert_config_equal(
            self.asteriskFrontEnd.queueskills_conf(),
            """
            [agent-1]
            test-skill = 10
            """,
        )
        find_agent_queue_skills_settings.assert_called_once_with()

    @patch('accent_dao.asterisk_conf_dao.find_queue_skillrule_settings')
    def test_queueskillrules_conf(self, find_queue_skillrule_settings):
        find_queue_skillrule_settings.return_value = [
            {'id': 1, 'name': 'test-rule-1', 'rule': 'rule-1;rule-2'},
            {'id': 2, 'name': 'test-rule-2', 'rule': 'rule-3;rule-4'},
        ]
        assert_config_equal(
            self.asteriskFrontEnd.queueskillrules_conf(),
            """
            [skillrule-1]
            rule = rule-1
            rule = rule-2

            [skillrule-2]
            rule = rule-3
            rule = rule-4
            """,
        )
        find_queue_skillrule_settings.assert_called_once_with()
