# Copyright 2023 Accent Communications

from . import confd


def associate(sip_uuid, templates, check=True):
    response = confd.endpoints.sip(sip_uuid).put(templates=templates)
    if check:
        response.assert_ok()


def dissociate(sip_uuid, check=True):
    response = confd.endpoints.sip(sip_uuid).put(templates=[])
    if check:
        response.assert_ok()
