# Copyright 2023 Accent Communications

from . import confd


def associate(user_id, call_permission_id, check=True):
    response = confd.users(user_id).callpermissions(call_permission_id).put()
    if check:
        response.assert_ok()


def dissociate(user_id, call_permission_id, check=True):
    response = confd.users(user_id).callpermissions(call_permission_id).delete()
    if check:
        response.assert_ok()
