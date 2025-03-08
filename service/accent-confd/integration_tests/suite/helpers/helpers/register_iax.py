# Copyright 2023 Accent Communications

from . import confd


def generate_register_iax(**params):
    params.setdefault('remote_host', 'remote-host-generated')
    return add_register_iax(**params)


def add_register_iax(**params):
    response = confd.registers.iax.post(params)
    return response.item


def delete_register_iax(register_iax_id, check=False, **params):
    response = confd.registers.iax(register_iax_id).delete()
    if check:
        response.assert_ok()
