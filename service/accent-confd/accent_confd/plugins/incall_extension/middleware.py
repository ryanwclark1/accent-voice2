# Copyright 2023 Accent Communications

from accent_dao.resources.extension import dao as extension_dao
from accent_dao.resources.incall import dao as incall_dao


class IncallExtensionAssociationMiddleWare:
    def __init__(self, service):
        self._service = service

    def associate(self, incall_id, extension_id, tenant_uuids):
        incall = incall_dao.get(incall_id, tenant_uuids=tenant_uuids)
        extension = extension_dao.get(extension_id, tenant_uuids=tenant_uuids)
        self._service.associate(incall, extension)

    def dissociate(self, incall_id, extension_id, tenant_uuids):
        incall = incall_dao.get(incall_id, tenant_uuids=tenant_uuids)
        extension = extension_dao.get(extension_id, tenant_uuids=tenant_uuids)
        self._service.dissociate(incall, extension)
