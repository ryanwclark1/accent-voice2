# Copyright 2023 Accent Communications

from . import confd


def add_iax(accent_tenant=None, **params):
    response = confd.endpoints.iax.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_iax(iax_id, check=False, **params):
    response = confd.endpoints.iax(iax_id).delete()
    if check:
        response.assert_ok()


def generate_iax(**params):
    return add_iax(**params)
