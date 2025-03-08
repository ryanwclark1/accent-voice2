# Copyright 2023 Accent Communications

from . import confd


def generate_incall(**params):
    params.setdefault('destination', {'type': 'none'})
    return add_incall(**params)


def add_incall(accent_tenant=None, **params):
    response = confd.incalls.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_incall(incall_id, check=False, **params):
    response = confd.incalls(incall_id).delete()
    if check:
        response.assert_ok()
