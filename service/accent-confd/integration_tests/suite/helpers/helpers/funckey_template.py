# Copyright 2023 Accent Communications

from . import confd


def generate_funckey_template(**params):
    return add_funckey_template(**params)


def add_funckey_template(accent_tenant=None, **params):
    response = confd.funckeys.templates.post(params, accent_tenant=accent_tenant)
    return response.item


def delete_funckey_template(funckey_template_id, check=False, **params):
    response = confd.funckeys.templates(funckey_template_id).delete()
    if check:
        response.assert_ok()
