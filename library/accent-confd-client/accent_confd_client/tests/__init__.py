# Copyright 2023 Accent Communications

from unittest import TestCase
from unittest.mock import Mock

from ..session import ConfdSession


class TestCommand(TestCase):
    def setUp(self):
        self.session = Mock(ConfdSession)
        self.session.READ_HEADERS = ConfdSession.READ_HEADERS
        self.session.WRITE_HEADERS = ConfdSession.WRITE_HEADERS
        self.client = Mock()
        self.client.session.return_value = self.session
        self.command = self.Command(self.client)

    def set_response(self, action, status_code, json=None, content=None):
        response = Mock()
        response.status_code = status_code
        response.json.return_value = json
        response.content = content

        mock_action = getattr(self.session, action)
        mock_action.return_value = response

        return json
