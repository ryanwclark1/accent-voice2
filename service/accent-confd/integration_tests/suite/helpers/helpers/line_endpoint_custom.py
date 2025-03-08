# Copyright 2023 Accent Communications

from . import confd


def associate(line_id, endpoint_id, check=True):
    response = confd.lines(line_id).endpoints.custom(endpoint_id).put()
    if check:
        response.assert_ok()


def dissociate(line_id, endpoint_id, check=True):
    response = confd.lines(line_id).endpoints.custom(endpoint_id).delete()
    if check:
        response.assert_ok()
