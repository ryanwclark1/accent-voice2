# Copyright 2023 Accent Communications

from . import confd


def associate(trunk_id, endpoint_id, check=True):
    response = confd.trunks(trunk_id).endpoints.sip(endpoint_id).put()
    if check:
        response.assert_ok()


def dissociate(trunk_id, endpoint_id, check=True):
    response = confd.trunks(trunk_id).endpoints.sip(endpoint_id).delete()
    if check:
        response.assert_ok()
