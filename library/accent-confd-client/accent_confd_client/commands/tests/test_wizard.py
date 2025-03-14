# Copyright 2023 Accent Communications

from accent_confd_client.tests import TestCommand

from ..wizard import WizardCommand


class TestWizard(TestCommand):
    Command = WizardCommand

    def test_create(self):
        body = {'admin_password': 'password', 'etc': '...'}

        expected_content = {'accent_uuid': 'UUID'}
        expected_url = "/wizard"

        self.set_response('post', 204, expected_content)

        self.command.create(body, timeout=600)

        self.session.post.assert_called_once_with(expected_url, body, timeout=600)

    def test_get(self):
        expected_content = {'configured': False}
        expected_url = "/wizard"
        self.set_response('get', 200, expected_content)

        self.command.get()

        self.session.get.assert_called_once_with(expected_url)

    def test_discover(self):
        expected_url = "/wizard/discover"
        expected_content = {'hostname': 'accent', 'etc': '...'}

        self.set_response('get', 200, expected_content)

        self.command.discover()

        self.session.get.assert_called_once_with(expected_url)
