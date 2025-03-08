# Copyright 2023 Accent Communications

from accent_dao.helpers import errors
from accent_dao.resources.line import dao as line_dao_module

from accent_confd.database import device as device_db

from .notifier import build_notifier
from .validator import build_validator


class LineDevice:
    @classmethod
    def from_line(cls, line):
        return cls(line.id, line.device_id)

    def __init__(self, line_id, device_id):
        self.line_id = line_id
        self.device_id = device_id


class LineDeviceService:
    def __init__(self, validator, line_dao, notifier, device_updater):
        self.validator = validator
        self.line_dao = line_dao
        self.notifier = notifier
        self.device_updater = device_updater

    def associate(self, line, device):
        if line.device_id == device.id:
            return

        self.validator.validate_association(line, device)
        self.associate_line_device(line, device)
        self.notifier.associated(line, device)

    def associate_line_device(self, line, device):
        line.associate_device(device)
        self.device_updater.update_device(device, tenant_uuid=line.tenant_uuid)
        if line.endpoint_sccp_id:
            device_db.associate_sccp_device(line, device)

    def dissociate(self, line, device):
        if line.device_id != device.id:
            return

        self.validator.validate_dissociation(line, device)
        self.dissociate_line_device(line, device)
        self.device_updater.update_device(device, tenant_uuid=line.tenant_uuid)
        self.notifier.dissociated(line, device)

    def dissociate_line_device(self, line, device):
        line.remove_device()
        self.device_updater.update_device(device, tenant_uuid=line.tenant_uuid)
        if line.endpoint_sccp_id:
            device_db.dissociate_sccp_device(line, device)

    def get_association_from_line(self, line):
        if not line.device_id:
            raise errors.not_found('LineDevice', line_id=line.id)
        return LineDevice.from_line(line)

    def find_all_associations_from_device(self, device):
        lines = self.line_dao.find_all_by(device=device.id)
        return [LineDevice.from_line(line) for line in lines]


def build_service(provd_client, device_updater):
    validator = build_validator()
    notifier = build_notifier()
    return LineDeviceService(validator, line_dao_module, notifier, device_updater)
