# Copyright 2023 Accent Communications

from .notifier import build_notifier
from .validator import build_validator


class OutcallScheduleService:
    def __init__(self, notifier, validator):
        self.validator = validator
        self.notifier = notifier

    def associate(self, outcall, schedule):
        if schedule in outcall.schedules:
            return

        self.validator.validate_association(outcall, schedule)
        outcall.schedules = [schedule]
        self.notifier.associated(outcall, schedule)

    def dissociate(self, outcall, schedule):
        if schedule not in outcall.schedules:
            return

        self.validator.validate_dissociation(outcall, schedule)
        outcall.schedules = []
        self.notifier.dissociated(outcall, schedule)


def build_service():
    return OutcallScheduleService(build_notifier(), build_validator())
