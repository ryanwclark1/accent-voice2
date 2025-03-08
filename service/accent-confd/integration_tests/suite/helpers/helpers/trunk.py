# Copyright 2023 Accent Communications

from . import confd


def generate_trunk(**params):
    return add_trunk(**params)


def add_trunk(accent_tenant=None, **params):
    response = confd.trunks.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_trunk(trunk_id, check=False, **params):
    response = confd.trunks(trunk_id).delete()
    if check:
        response.assert_ok()
