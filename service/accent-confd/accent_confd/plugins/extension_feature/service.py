# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import Session
from accent_dao.resources.feature_extension import dao as feature_extension_dao

from accent_confd.helpers.resource import CRUDService

from .notifier import build_notifier
from .validator import build_validator


class FeatureExtensionService(CRUDService):
    def search(self, parameters):
        return self.dao.search(**parameters)

    def get(self, resource_uuid):
        return self.dao.get_by(uuid=resource_uuid)

    def edit(self, resource, updated_fields=None):
        with Session.no_autoflush:
            self.validator.validate_edit(resource)
        self.dao.edit(resource)
        self.notifier.edited(resource, updated_fields)


def build_service():
    return FeatureExtensionService(
        feature_extension_dao, build_validator(), build_notifier()
    )
