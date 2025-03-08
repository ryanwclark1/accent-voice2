# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import Session

from .notifier import build_notifier
from .validator import build_validator


class GroupFallbackService:
    def __init__(self, notifier, validator):
        self.validator = validator
        self.notifier = notifier

    def edit(self, group, fallbacks):
        with Session.no_autoflush:
            self.validator.validate_edit(fallbacks)
        group.fallbacks = fallbacks
        self.notifier.edited(group)


def build_service():
    return GroupFallbackService(build_notifier(), build_validator())
