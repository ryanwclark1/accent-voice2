# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock, patch
from unittest.mock import sentinel as s

from ..tenant_flask_helpers import Tenant
from ..tenant_flask_helpers import auth_client as auth_client_proxy


class TestAuthClient(unittest.TestCase):
    @patch("accent.tenant_flask_helpers.AuthClient")
    def test_config_deleted(self, auth_client):
        g_mock = Mock()
        g_mock.get.return_value = None
        config = {
            "host": s.host,
            "username": s.username,
            "password": s.password,
            "key_file": s.key_file,
        }
        current_app_mock = Mock(config={"auth": config})

        with patch("accent.tenant_flask_helpers.current_app", current_app_mock):
            with patch("accent.tenant_flask_helpers.g", g_mock):
                auth_client_proxy.host

        expected_config = {"host": s.host}
        auth_client.assert_called_once_with(**expected_config)


class TestTenant(unittest.TestCase):
    @patch("accent.tenant_flask_helpers.AuthClient")
    def test_autodetect_when_verified_tenant_uuid(self, auth_client):
        g_mock = Mock()
        g_data = {"verified_tenant_uuid": s.tenant}
        g_mock.get.side_effect = lambda x: g_data[x]
        request_mock = Mock()
        request_mock.headers.get.return_value = s.tenant
        request_mock.args = []

        with patch("accent.tenant_flask_helpers.g", g_mock):
            with patch("accent.flask.headers.request", request_mock):
                tenant = Tenant.autodetect()

        assert tenant.uuid == s.tenant
