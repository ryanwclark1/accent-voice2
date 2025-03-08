# Copyright 2023 Accent Communications

from .notifier import build_notifier
from .validator import build_validator


class SwitchboardMemberUserService:
    def __init__(self, notifier, validator):
        self.validator = validator
        self.notifier = notifier

    def associate_all_member_users(self, switchboard, users):
        self.validator.validate_association(switchboard, users)

        switchboard.user_members = set(users)

        self.notifier.members_associated(switchboard, users)


def build_service():
    return SwitchboardMemberUserService(build_notifier(), build_validator())
