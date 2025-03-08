# Copyright 2023 Accent Communications

from . import confd


def associate(outcall_id, call_permission_id, check=True):
    response = confd.outcalls(outcall_id).callpermissions(call_permission_id).put()
    if check:
        response.assert_ok()


def dissociate(outcall_id, call_permission_id, check=True):
    response = confd.outcalls(outcall_id).callpermissions(call_permission_id).delete()
    if check:
        response.assert_ok()
