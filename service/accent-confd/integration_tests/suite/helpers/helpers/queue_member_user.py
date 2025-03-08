# Copyright 2023 Accent Communications

from . import confd


def associate(queue_id, user_id, **kwargs):
    check = kwargs.pop('check', True)
    response = confd.queues(queue_id).members.users(user_id).put(**kwargs)
    if check:
        response.assert_ok()


def dissociate(queue_id, user_id, **kwargs):
    check = kwargs.get('check', True)
    response = confd.queues(queue_id).members.users(user_id).delete()
    if check:
        response.assert_ok()
