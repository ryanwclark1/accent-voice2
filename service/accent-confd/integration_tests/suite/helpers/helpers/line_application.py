# Copyright 2023 Accent Communications

from . import confd


def associate(line_id, application_uuid, check=True):
    response = confd.lines(line_id).applications(application_uuid).put()
    if check:
        response.assert_ok()


def dissociate(line_id, application_uuid, check=True):
    response = confd.lines(line_id).applications(application_uuid).delete()
    if check:
        response.assert_ok()
