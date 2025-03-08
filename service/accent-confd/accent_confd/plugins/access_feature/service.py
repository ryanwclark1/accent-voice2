# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import Session
from accent_dao.resources.access_feature import dao as access_feature_dao

from accent_confd.helpers.resource import CRUDService

from .notifier import build_notifier
from .validator import build_validator


class AccessFeatureService(CRUDService):
    def create(self, access_feature):
        self.validator.validate_create(access_feature)
        created_access_feature = self.dao.create(access_feature)
        self.notifier.created(created_access_feature)
        return created_access_feature

    def edit(self, access_feature, updated_fields=None):
        with Session.no_autoflush:
            self.validator.validate_edit(access_feature)
        self.dao.edit(access_feature)
        self.notifier.edited(access_feature)


def build_service():
    return AccessFeatureService(access_feature_dao, build_validator(), build_notifier())
