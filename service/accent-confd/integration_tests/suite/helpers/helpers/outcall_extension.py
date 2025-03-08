# Copyright 2023 Accent Communications

from . import confd


def associate(outcall_id, extension_id, **kwargs):
    check = kwargs.pop('check', True)
    response = confd.outcalls(outcall_id).extensions(extension_id).put(**kwargs)
    if check:
        response.assert_ok()


def dissociate(outcall_id, extension_id, **kwargs):
    check = kwargs.get('check', True)
    response = confd.outcalls(outcall_id).extensions(extension_id).delete()
    if check:
        response.assert_ok()
