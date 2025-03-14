# Copyright 2023 Accent Communications

import random
import string

from . import confd


def add_custom(accent_tenant=None, **params):
    response = confd.endpoints.custom.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_custom(custom_id, check=False, **params):
    response = confd.endpoints.custom(custom_id).delete()
    if check:
        response.assert_ok()


def generate_custom(**params):
    name = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
    params.setdefault('interface', 'custom/{}'.format(name))
    return add_custom(**params)
