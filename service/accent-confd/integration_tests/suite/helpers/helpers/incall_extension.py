# Copyright 2023 Accent Communications

from . import confd


def associate(incall_id, extension_id, check=True):
    response = confd.incalls(incall_id).extensions(extension_id).put()
    if check:
        response.assert_ok()


def dissociate(incall_id, extension_id, check=True):
    response = confd.incalls(incall_id).extensions(extension_id).delete()
    if check:
        response.assert_ok()
