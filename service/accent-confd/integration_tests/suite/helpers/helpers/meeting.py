# Copyright 2023 Accent Communications

from . import confd


def add(accent_tenant=None, **params):
    response = confd.meetings.post(params, accent_tenant=accent_tenant)
    return response.item


def delete(uuid, check=False, **params):
    response = confd.meetings(uuid).delete()
    if check:
        response.assert_ok()


def generate(**params):
    params.setdefault('name', 'meeting')
    return add(**params)
