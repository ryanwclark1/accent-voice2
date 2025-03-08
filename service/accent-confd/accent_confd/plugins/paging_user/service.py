# Copyright 2023 Accent Communications

from accent_dao.resources.paging import dao as paging_dao_module

from .notifier import build_notifier
from .validator import build_validator


class PagingUserService:
    def __init__(self, paging_dao, notifier, validator):
        self.paging_dao = paging_dao
        self.validator = validator
        self.notifier = notifier

    def associate_all_caller_users(self, paging, users):
        self.validator.validate_association(paging, users)
        paging.users_caller = users
        self.notifier.callers_associated(paging, users)

    def associate_all_member_users(self, paging, users):
        self.validator.validate_association(paging, users)
        paging.users_member = users
        self.notifier.members_associated(paging, users)


def build_service():
    return PagingUserService(paging_dao_module, build_notifier(), build_validator())
