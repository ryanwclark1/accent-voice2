# Copyright 2023 Accent Communications

import random
import string

from . import confd


def generate_sound(**parameters):
    parameters.setdefault('name', generate_name())
    return add_sound(**parameters)


def add_sound(accent_tenant=None, **parameters):
    name = parameters.get('name')
    files = parameters.pop('files', [])
    response = confd.sounds.post(parameters, accent_tenant=accent_tenant)
    if files:
        _generate_files(name, files, accent_tenant=accent_tenant)
        response = confd.sounds(name).get(accent_tenant=accent_tenant)
    return response.item


def delete_sound(sound_name, check=False, accent_tenant=None, **kwargs):
    response = confd.sounds(sound_name).delete(accent_tenant=accent_tenant)
    if check:
        response.assert_ok()


def generate_name():
    response = confd.sounds.get()
    forbidden_names = set(d['name'] for d in response.items)
    return _random_name(forbidden_names)


def _random_name(forbidden_names):
    name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    if name in forbidden_names:
        return _random_name(forbidden_names)
    return name


def _generate_files(sound_name, files, accent_tenant=None):
    for file in files:
        file_name = file.pop('name', generate_name())
        confd.sounds(sound_name).files(file_name).put(
            accent_tenant=accent_tenant, content='Some content', query_string=file
        ).assert_ok()
