# Copyright 2023 Accent Communications

from .. import config
from . import confd


def add_line(accent_tenant=None, **params):
    response = confd.lines.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_line(line_id, check=False, **params):
    response = confd.lines(line_id).delete()
    if check:
        response.assert_ok()


def generate_line(**params):
    params.setdefault('context', config.CONTEXT)
    return add_line(**params)
