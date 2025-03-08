# Copyright 2023 Accent Communications

from . import confd


def add_sip(accent_tenant=None, **params):
    response = confd.endpoints.sip.post(params, accent_tenant=accent_tenant)
    return response.item


def add_sip_template(accent_tenant=None, **params):
    response = confd.endpoints.sip.templates.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_sip(sip_uuid, check=False, **params):
    response = confd.endpoints.sip(sip_uuid).delete()
    if check:
        response.assert_ok()


def delete_sip_template(sip_template_uuid, check=False, **params):
    response = confd.endpoints.sip.templates(sip_template_uuid).delete()
    if check:
        response.assert_ok()


def generate_sip(**params):
    return add_sip(**params)


def generate_sip_template(**params):
    return add_sip_template(**params)
