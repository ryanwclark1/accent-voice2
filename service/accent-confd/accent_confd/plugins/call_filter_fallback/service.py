# Copyright 2023 Accent Communications

from accent_dao.helpers.db_manager import Session
from accent_dao.resources.call_filter import dao as call_filter_dao

from .notifier import build_notifier
from .validator import build_validator


class CallFilterFallbackService:
    def __init__(self, dao, notifier, validator):
        self.call_filter_dao = dao
        self.notifier = notifier
        self.validator = validator

    def edit(self, call_filter, fallbacks):
        with Session.no_autoflush:
            self.validator.validate_edit(fallbacks)
        self.call_filter_dao.update_fallbacks(call_filter, fallbacks)
        self.notifier.edited(call_filter)


def build_service():
    return CallFilterFallbackService(
        call_filter_dao, build_notifier(), build_validator()
    )
