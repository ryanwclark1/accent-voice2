# Copyright 2023 Accent Communications

from ..config import CONTEXT, USER_EXTENSION_RANGE
from . import confd


def generate_extension(**parameters):
    parameters.setdefault('context', CONTEXT)
    parameters.setdefault('exten', find_available_exten(parameters['context']))
    return add_extension(**parameters)


def find_available_exten(context, exclude=None):
    exclude = {int(n) for n in exclude} if exclude else set()
    response = confd.extensions.get()
    numbers = [
        int(e['exten'])
        for e in response.items
        if e['context'] == context and e['exten'].isdigit()
    ]

    available = set(USER_EXTENSION_RANGE) - set(numbers) - exclude
    return str(available.pop())


def add_extension(accent_tenant=None, **params):
    response = confd.extensions.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_extension(extension_id, check=False, **params):
    response = confd.extensions(extension_id).delete()
    if check:
        response.assert_ok()
