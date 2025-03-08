# Copyright 2023 Accent Communications

from accent_dao.resources.line import dao as line_dao


class LineDeviceAssociationMiddleWare:
    def __init__(self, service, device_dao):
        self._service = service
        self._device_dao = device_dao

    def associate(self, line_id, device_id, tenant_uuid, tenant_uuids):
        line = line_dao.get(line_id, tenant_uuids=tenant_uuids)
        device = self._device_dao.get(device_id, tenant_uuid=tenant_uuid)
        self._service.associate(line, device)

    def dissociate(self, line_id, device_id, tenant_uuid, tenant_uuids):
        line = line_dao.get(line_id, tenant_uuids=tenant_uuids)
        device = self._device_dao.get(device_id, tenant_uuid=tenant_uuid)
        self._service.dissociate(line, device)
