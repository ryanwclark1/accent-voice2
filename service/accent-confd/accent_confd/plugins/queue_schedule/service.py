# Copyright 2023 Accent Communications

from .notifier import build_notifier
from .validator import build_validator


class QueueScheduleService:
    def __init__(self, queue_dao, notifier, validator):
        self.queue_dao = queue_dao
        self.validator = validator
        self.notifier = notifier

    def associate(self, queue, schedule):
        if schedule in queue.schedules:
            return

        self.validator.validate_association(queue, schedule)
        self.queue_dao.associate_schedule(queue, schedule)
        self.notifier.associated(queue, schedule)

    def dissociate(self, queue, schedule):
        if schedule not in queue.schedules:
            return

        self.validator.validate_dissociation(queue, schedule)
        self.queue_dao.dissociate_schedule(queue, schedule)
        self.notifier.dissociated(queue, schedule)


def build_service(queue_dao):
    return QueueScheduleService(queue_dao, build_notifier(), build_validator())
