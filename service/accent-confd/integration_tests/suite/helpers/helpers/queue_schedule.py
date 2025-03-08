# Copyright 2023 Accent Communications

from . import confd


def associate(queue_id, schedule_id, check=True):
    response = confd.queues(queue_id).schedules(schedule_id).put()
    if check:
        response.assert_ok()


def dissociate(queue_id, schedule_id, check=True):
    response = confd.queues(queue_id).schedules(schedule_id).delete()
    if check:
        response.assert_ok()
