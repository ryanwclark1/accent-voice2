# Copyright 2023 Accent Communications

from . import confd


def associate(transport_uuid, endpoint_uuid, check=True):
    response = confd.endpoints.sip(endpoint_uuid).put(
        transport={'uuid': transport_uuid},
    )
    if check:
        response.assert_ok()


def dissociate(transport_uuid, endpoint_uuid, check=True):
    response = confd.endpoints.sip(endpoint_uuid).put(
        transport=None,
    )
    if check:
        response.assert_ok()
