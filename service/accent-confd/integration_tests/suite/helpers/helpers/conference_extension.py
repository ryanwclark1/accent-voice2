# Copyright 2023 Accent Communications


from . import confd


def associate(conference_id, extension_id, check=True):
    response = confd.conferences(conference_id).extensions(extension_id).put()
    if check:
        response.assert_ok()


def dissociate(conference_id, extension_id, check=True):
    response = confd.conferences(conference_id).extensions(extension_id).delete()
    if check:
        response.assert_ok()
