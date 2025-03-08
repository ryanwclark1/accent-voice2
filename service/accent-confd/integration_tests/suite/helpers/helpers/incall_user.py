# Copyright 2023 Accent Communications

from . import confd


def associate(incall_id, user_id, check=True):
    response = confd.incalls(incall_id).put(
        destination={'type': 'user', 'user_id': user_id}
    )
    if check:
        response.assert_ok()


def dissociate(incall_id, extension_id, check=True):
    response = confd.incalls(incall_id).put(destination={'type': 'none'})
    if check:
        response.assert_ok()
