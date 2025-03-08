# Copyright 2023 Accent Communications

from . import confd


def associate(outcall_id, schedule_id, check=True):
    response = confd.outcalls(outcall_id).schedules(schedule_id).put()
    if check:
        response.assert_ok()


def dissociate(outcall_id, schedule_id, check=True):
    response = confd.outcalls(outcall_id).schedules(schedule_id).delete()
    if check:
        response.assert_ok()
