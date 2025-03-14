# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from unittest.mock import sentinel as s

from ..importer import AccentAPI


class TestAccentAPI(unittest.TestCase):
    def test_authenticate(self):
        api = AccentAPI(s.username, s.password, tenant_uuid=s.tenant)
        api._auth_client = Mock()
        api._confd_client = Mock()

        api._auth_client.token.new.return_value = {"token": s.token}

        api.authenticate()

        api._auth_client.set_token.assert_called_once_with(s.token)
        api._auth_client.set_token.assert_called_once_with(s.token)

    def test_set_tenant_with_tenant(self):
        api = AccentAPI(s.username, s.password, tenant_uuid=s.tenant)
        api._auth_client = Mock()
        api._confd_client = Mock()

        api.set_tenant()

        assert api._auth_client.tenant_uuid == s.tenant
        assert api._confd_client.tenant_uuid == s.tenant

    def test_set_tenant_with_new_tenant(self):
        api = AccentAPI(s.username, s.password, tenant_slug=s.tenant_slug)
        api._auth_client = Mock()
        api._confd_client = Mock()

        api._auth_client.tenants.new.return_value = {"uuid": s.tenant_uuid}

        api.set_tenant()

        api._auth_client.tenants.new.assert_called_once_with(
            name=s.tenant_slug,
            slug=s.tenant_slug,
        )
        assert api._auth_client.tenant_uuid == s.tenant_uuid
        assert api._confd_client.tenant_uuid == s.tenant_uuid
        assert api._tenant_uuid == s.tenant_uuid
