# Copyright 2023 Accent Communications

from . import confd


def associate(incall_id, schedule_id, check=True):
    response = confd.incalls(incall_id).schedules(schedule_id).put()
    if check:
        response.assert_ok()


def dissociate(incall_id, schedule_id, check=True):
    response = confd.incalls(incall_id).schedules(schedule_id).delete()
    if check:
        response.assert_ok()
