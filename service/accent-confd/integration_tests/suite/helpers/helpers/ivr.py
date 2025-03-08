# Copyright 2023 Accent Communications

import random
import string

from . import confd


def generate_ivr(**parameters):
    parameters.setdefault('name', _random_name())
    parameters.setdefault('menu_sound', 'hello-world')
    return add_ivr(**parameters)


def add_ivr(accent_tenant=None, **parameters):
    response = confd.ivr.post(parameters, accent_tenant=accent_tenant)
    return response.item


def delete_ivr(ivr_id, check=False, **parameters):
    response = confd.ivr(ivr_id).delete()
    if check:
        response.assert_ok()


def _random_name():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
