# Copyright 2023 Accent Communications

from . import confd


def associate(group_id, call_permission_id, check=True):
    response = confd.groups(group_id).callpermissions(call_permission_id).put()
    if check:
        response.assert_ok()


def dissociate(group_id, call_permission_id, check=True):
    response = confd.groups(group_id).callpermissions(call_permission_id).delete()
    if check:
        response.assert_ok()
