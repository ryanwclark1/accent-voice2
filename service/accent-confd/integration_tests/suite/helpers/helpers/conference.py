# Copyright 2023 Accent Communications

from . import confd


def generate_conference(**parameters):
    return add_conference(**parameters)


def add_conference(accent_tenant=None, **parameters):
    response = confd.conferences.post(parameters, accent_tenant=accent_tenant)
    return response.item


def delete_conference(conference_id, check=False, **params):
    response = confd.conferences(conference_id).delete()
    if check:
        response.assert_ok()
