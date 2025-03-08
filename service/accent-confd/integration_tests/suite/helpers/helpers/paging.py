# Copyright 2023 Accent Communications

import random
import string

from . import confd


def generate_paging(**parameters):
    parameters.setdefault('number', _generate_number())
    return add_paging(**parameters)


def _generate_number():
    response = confd.pagings.get()
    numbers = set(d['number'] for d in response.items)
    return _random_number(numbers)


def _random_number(numbers):
    number = ''.join(random.choice(string.digits) for _ in range(3))
    if number in numbers:
        return _random_number(numbers)
    return number


def add_paging(accent_tenant=None, **parameters):
    response = confd.pagings.post(parameters, accent_tenant=accent_tenant)
    return response.item


def delete_paging(paging_id, check=False, **parameters):
    response = confd.pagings(paging_id).delete()
    if check:
        response.assert_ok()
