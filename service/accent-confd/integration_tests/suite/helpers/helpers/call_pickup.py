# Copyright 2023 Accent Communications

import random
import string

from . import confd


def generate_call_pickup(**params):
    params.setdefault('name', generate_name())
    return add_call_pickup(**params)


def add_call_pickup(accent_tenant=None, **params):
    response = confd.callpickups.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_call_pickup(call_pickup_id, check=False, **params):
    response = confd.callpickups(call_pickup_id).delete()
    if check:
        response.assert_ok()


def generate_name():
    response = confd.callpickups.get()
    names = set(d['name'] for d in response.items)
    return _random_name(names)


def _random_name(names):
    name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    while name in names:
        name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    return name
