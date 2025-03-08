# Copyright 2023 Accent Communications

from accent_dao.helpers import errors

from accent_confd.plugins.device.schema import DeviceSchema


class DeviceMiddleWare:
    def __init__(self, service):
        self._service = service
        self._schema = DeviceSchema()

    def assign_tenant(self, device_id, tenant_uuid):
        device = self._service.get(device_id)
        if not device.is_new:
            raise errors.not_found('Device', id=device_id)
        self._service.assign_tenant(device, tenant_uuid=tenant_uuid)

    def reset_autoprov(self, device_id, tenant_uuid):
        device = self._service.get(device_id, tenant_uuid=tenant_uuid)
        self._service.reset_autoprov(device, tenant_uuid=tenant_uuid)

    def get(self, device_id, tenant_uuid):
        model = self._service.get(device_id, tenant_uuid=tenant_uuid)
        return self._schema.dump(model)
