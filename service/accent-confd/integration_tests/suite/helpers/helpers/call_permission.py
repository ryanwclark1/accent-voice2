# Copyright 2023 Accent Communications

import random
import string

from . import confd


def generate_call_permission(**params):
    name = generate_name()
    params.setdefault('name', name)
    return add_call_permission(**params)


def add_call_permission(accent_tenant=None, **params):
    response = confd.callpermissions.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_call_permission(call_permission_id, check=False, **params):
    response = confd.callpermissions(call_permission_id).delete()
    if check:
        response.assert_ok()


def generate_name():
    response = confd.callpermissions.get()
    names = set(d['name'] for d in response.items)
    return _random_name(names)


def _random_name(names):
    name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    while name in names:
        name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    return name
