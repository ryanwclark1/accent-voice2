# Copyright 2023 Accent Communications

from . import confd


def generate_ingress_http(**parameters):
    parameters.setdefault('uri', 'https://test.example.com')
    return add_ingress_http(**parameters)


def delete_ingress_http(uuid, check=False, **parameters):
    response = confd.ingresses.http(uuid).delete()
    if check:
        response.assert_ok()


def add_ingress_http(accent_tenant=None, **parameters):
    response = confd.ingresses.http.post(parameters, accent_tenant=accent_tenant)
    return response.item
