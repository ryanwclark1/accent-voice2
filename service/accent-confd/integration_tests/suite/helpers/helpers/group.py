# Copyright 2023 Accent Communications

import random
import string

from . import confd


def generate_group(**parameters):
    parameters.setdefault('label', generate_name())
    return add_group(**parameters)


def add_group(accent_tenant=None, **parameters):
    response = confd.groups.post(parameters, accent_tenant=accent_tenant)
    return response.item


def delete_group(group_id, check=False, **parameters):
    response = confd.groups(group_id).delete()
    if check:
        response.assert_ok()


def generate_name():
    response = confd.groups.get()
    names = set(d['name'] for d in response.items)
    return _random_name(names)


def _random_name(names):
    name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    if name in names:
        return _random_name(names)
    return name
