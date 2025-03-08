# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import Session

from .notifier import build_notifier
from .validator import build_validator


class UserFallbackService:
    def __init__(self, notifier, validator):
        self.validator = validator
        self.notifier = notifier

    def edit(self, user, fallbacks):
        with Session.no_autoflush:
            self.validator.validate_edit(fallbacks)
        user.fallbacks = fallbacks
        self.notifier.edited(user)


def build_service():
    return UserFallbackService(build_notifier(), build_validator())
