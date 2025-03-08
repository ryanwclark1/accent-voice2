# Copyright 2023 Accent Communications

from . import confd


def add_sccp(accent_tenant=None, **params):
    response = confd.endpoints.sccp.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_sccp(sccp_id, check=False, **params):
    response = confd.endpoints.sccp(sccp_id).delete()
    if check:
        response.assert_ok()


def generate_sccp(**params):
    return add_sccp(**params)
