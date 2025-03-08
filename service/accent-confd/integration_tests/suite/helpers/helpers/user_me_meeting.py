# Copyright 2023 Accent Communications

from . import confd


def add(confd_client, accent_tenant=None, **params):
    response = confd_client.users.me.meetings.post(params, accent_tenant=accent_tenant)
    return response.item


def delete(uuid, check=False, **params):
    response = confd.meetings(uuid).delete()
    if check:
        response.assert_ok()


def generate(confd_client, **params):
    params.setdefault('name', 'meeting')
    return add(confd_client, **params)
