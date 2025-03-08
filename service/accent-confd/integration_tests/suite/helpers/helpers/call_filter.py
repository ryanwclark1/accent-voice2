# Copyright 2023 Accent Communications

import random
import string

from . import confd


def generate_call_filter(**params):
    name = generate_name()
    params.setdefault('name', name)
    params.setdefault('source', 'all')
    params.setdefault('strategy', 'all')
    return add_call_filter(**params)


def add_call_filter(accent_tenant=None, **params):
    response = confd.callfilters.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_call_filter(call_filter_id, check=False, **kwargs):
    response = confd.callfilters(call_filter_id).delete()
    if check:
        response.assert_ok()


def generate_name():
    response = confd.callfilters.get()
    names = set(d['name'] for d in response.items)
    return _random_name(names)


def _random_name(names):
    name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    while name in names:
        name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    return name
