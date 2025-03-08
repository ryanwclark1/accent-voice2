# Copyright 2023 Accent Communications

from . import confd


def associate(user_id, schedule_id, check=True):
    response = confd.users(user_id).schedules(schedule_id).put()
    if check:
        response.assert_ok()


def dissociate(user_id, schedule_id, check=True):
    response = confd.users(user_id).schedules(schedule_id).delete()
    if check:
        response.assert_ok()
