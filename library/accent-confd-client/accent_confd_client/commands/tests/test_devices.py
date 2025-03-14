# Copyright 2023 Accent Communications

from hamcrest import assert_that, equal_to

from accent_confd_client.tests import TestCommand

from ..devices import DevicesCommand, UnallocatedDevicesCommand


class TestDevices(TestCommand):
    Command = DevicesCommand

    def test_autoprov(self):
        device_id = "a1b2c3d4e5f6g7h8i9j0k1l2"
        expected_url = f"/devices/{device_id}/autoprov"
        expected_headers = {
            'Accept': 'application/json',
        }
        self.client.tenant_uuid = None
        self.set_response('get', 204)

        self.command.autoprov(device_id)

        self.session.get.assert_called_once_with(expected_url, headers=expected_headers)

    def test_autoprov_with_tenant(self):
        device_id = "a1b2c3d4e5f6g7h8i9j0k1l2"
        expected_url = f"/devices/{device_id}/autoprov"
        expected_headers = {
            'Accept': 'application/json',
            'Accent-Tenant': 'tenant',
        }
        self.client.tenant_uuid = 'tenant'
        self.set_response('get', 204)

        self.command.autoprov(device_id)

        self.session.get.assert_called_once_with(expected_url, headers=expected_headers)

    def test_synchronize(self):
        device_id = "a1b2c3d4e5f6g7h8i9j0k1l2"
        expected_url = f"/devices/{device_id}/synchronize"
        expected_headers = {
            'Accept': 'application/json',
        }
        self.client.tenant_uuid = None
        self.set_response('get', 204)

        self.command.synchronize(device_id)

        self.session.get.assert_called_once_with(expected_url, headers=expected_headers)

    def test_synchronize_with_tenants(self):
        device_id = "a1b2c3d4e5f6g7h8i9j0k1l2"
        expected_url = f"/devices/{device_id}/synchronize"
        expected_headers = {
            'Accept': 'application/json',
            'Accent-Tenant': 'tenant',
        }
        self.client.tenant_uuid = 'tenant'
        self.set_response('get', 204)

        self.command.synchronize(device_id)

        self.session.get.assert_called_once_with(expected_url, headers=expected_headers)


class TestUnallocatedDevices(TestCommand):
    Command = UnallocatedDevicesCommand

    def test_unallocated_listing(self):
        expected_url = "/devices/unallocated"
        self.client.tenant_uuid = None
        expected_response = self.set_response(
            'get', 200, {"total": 2, "items": [{"device": {}}, {"device": {}}]}
        )

        result = self.command.list(search='term')
        assert_that(result, equal_to(expected_response))

        self.session.get.assert_called_once_with(
            expected_url, params={'search': 'term'}
        )

    def test_assign_tenant(self):
        device_id = 'a1b2c3d4e5f6g7h8i9j0k1l9'
        expected_url = f"/devices/unallocated/{device_id}"
        expected_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Accent-Tenant': 'tenant',
        }
        self.client.tenant_uuid = 'tenant'
        self.set_response('put', 204)

        self.command.assign_tenant(device_id)
        self.session.put.assert_called_once_with(expected_url, headers=expected_headers)
