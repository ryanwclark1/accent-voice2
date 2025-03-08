# Copyright 2023 Accent Communications

from accent_dao.resources.user import dao as user_dao_module

from .notifier import build_notifier
from .validator import build_validator


class UserGroupService:
    def __init__(self, user_dao, notifier, validator):
        self.user_dao = user_dao
        self.validator = validator
        self.notifier = notifier

    def associate_all_groups(self, user, groups):
        self.validator.validate_association(user, groups)
        self.user_dao.associate_all_groups(user, groups)
        self.notifier.associated(user, groups)


def build_service():
    return UserGroupService(user_dao_module, build_notifier(), build_validator())
