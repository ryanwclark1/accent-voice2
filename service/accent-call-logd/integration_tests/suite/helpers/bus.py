# Copyright 2023 Accent Communications

from accent_test_helpers.bus import BusClient


class CallLogBusClient(BusClient):
    def send_linkedid_end(self, linkedid):
        payload = {
            'data': {
                'EventName': 'LINKEDID_END',
                'LinkedID': linkedid,
            },
            'name': 'CEL',
        }
        self.publish(payload, headers={'name': 'CEL'})

    def send_tenant_deleted(self, tenant_uuid):
        payload = {'data': {'uuid': tenant_uuid}, 'name': 'auth_tenant_deleted'}
        self.publish(payload, headers={'name': 'auth_tenant_deleted'})
