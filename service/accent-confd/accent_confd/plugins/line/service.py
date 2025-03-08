# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import Session
from accent_dao.resources.line import dao as line_dao_module

from accent_confd.helpers.resource import CRUDService
from accent_confd.plugins.device import builder as device_builder
from accent_confd.plugins.line_device.service import (
    build_service as line_device_build_service,
)
from accent_confd.plugins.registrar.dao import RegistrarDao
from accent_confd.plugins.user_line.service import (
    build_service as user_line_build_service,
)

from .notifier import build_notifier
from .validator import build_validator


class LineService(CRUDService):
    def __init__(
        self,
        dao,
        validator,
        notifier,
        device_updater,
        device_dao,
        user_line_service,
        line_device_service,
    ):
        super().__init__(dao, validator, notifier)
        self.device_updater = device_updater
        self.device_dao = device_dao
        self.user_line_service = user_line_service
        self.line_device_service = line_device_service

    def find_by(self, **criteria):
        return self.dao.find_by(**criteria)

    def find_all_by(self, **criteria):
        return self.dao.find_all_by(**criteria)

    def create(self, resource, tenant_uuids):
        self.validator.validate_create(resource, tenant_uuids=tenant_uuids)
        created_resource = self.dao.create(resource)
        self.notifier.created(created_resource)
        return created_resource

    def edit(self, line, tenant_uuids, updated_fields=None):
        with Session.no_autoflush:
            self.validator.validate_edit(line, tenant_uuids=tenant_uuids)
        self.dao.edit(line)
        self.notifier.edited(line, updated_fields)
        self.device_updater.update_for_line(line)

    def delete(self, line):
        self.validator.validate_delete(line)
        if line.device_id:
            device = self.device_dao.get(line.device_id)
            self.line_device_service.dissociate(line, device)
        for user in line.users:
            self.user_line_service.dissociate(user, line)
        self.dao.delete(line)
        self.notifier.deleted(line)


def build_service(provd_client):
    device_dao = device_builder.build_dao(provd_client)
    device_updater = device_builder.build_device_updater(provd_client)
    registrar_dao = RegistrarDao(provd_client)

    return LineService(
        line_dao_module,
        build_validator(registrar_dao),
        build_notifier(),
        device_updater,
        device_dao,
        user_line_build_service(),
        line_device_build_service(provd_client, device_updater),
    )
