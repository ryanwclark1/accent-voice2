# Copyright 2023 Accent Communications

from . import confd


def associate(trunk_id, register_id, check=True):
    response = confd.trunks(trunk_id).registers.sip(register_id).put()
    if check:
        response.assert_ok()


def dissociate(trunk_id, register_id, check=True):
    response = confd.trunks(trunk_id).registers.sip(register_id).delete()
    if check:
        response.assert_ok()
