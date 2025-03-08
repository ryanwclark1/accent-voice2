# Copyright 2023 Accent Communications

from accent_dao.resources.features import dao as features_dao

from .notifier import build_notifier


class FeaturesConfigurationService:
    def __init__(self, dao, notifier):
        self.dao = dao
        self.notifier = notifier

    def list(self, section):
        return self.dao.find_all(section)

    def edit(self, section, variables):
        self.dao.edit_all(section, variables)
        self.notifier.edited(section, variables)


def build_service():
    return FeaturesConfigurationService(features_dao, build_notifier())
