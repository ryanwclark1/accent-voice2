# Copyright 2023 Accent Communications

from . import confd


def generate_application(**parameters):
    return add_application(**parameters)


def add_application(accent_tenant=None, **parameters):
    response = confd.applications.post(parameters, accent_tenant=accent_tenant)
    return response.item


def delete_application(application_uuid, check=False, **kwargs):
    response = confd.applications(application_uuid).delete()
    if check:
        response.assert_ok()
