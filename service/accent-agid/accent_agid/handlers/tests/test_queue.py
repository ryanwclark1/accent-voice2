# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock, patch

from hamcrest import assert_that, calling, equal_to, raises

from ..queue import AnswerHandler


class TestAnswerHandler(TestCase):
    def setUp(self):
        self.agi = Mock()
        self.cursor = Mock()
        self.args = Mock()

        self.handler = AnswerHandler(self.agi, self.cursor, self.args)

    @patch('accent_agid.handlers.queue.objects.User')
    def test_get_user_agent(self, User):
        agent_id = 42
        chan_name = f'Local/id-{agent_id}@agentcallback-0000000a1;1'
        self.agi.env = {
            'agi_channel': chan_name,
        }

        result = self.handler.get_user()

        assert_that(result, equal_to(User.return_value))
        User.assert_called_once_with(
            self.agi,
            self.cursor,
            agent_id=agent_id,
        )

    @patch('accent_agid.handlers.queue.objects.User')
    def test_get_user_user_member(self, User):
        user_uuid = 'e15b4765-719d-40d4-8bdd-ff578e2bef47'
        self.agi.env = {'agi_channel': f'Local/{user_uuid}@usersharedlines-00000001;1'}

        result = self.handler.get_user()

        assert_that(result, equal_to(User.return_value))
        User.assert_called_once_with(self.agi, self.cursor, xid=user_uuid)

    @patch('accent_agid.handlers.queue.objects.User')
    def test_get_user_unknown_user(self, User):
        User.side_effect = LookupError
        user_uuid = 'unknown    '
        self.agi.env = {
            'agi_channel': f'Local/{user_uuid}@usersharedlines-00000001;1',
        }

        assert_that(calling(self.handler.get_user), raises(LookupError))

    def test_get_user_how_did_that_happen(self):
        self.agi.get_variable.return_value = ''
        self.agi.env = {'agi_channel': 'PJSIP/wedontcare-00000001;1'}

        assert_that(calling(self.handler.get_user), raises(LookupError))
