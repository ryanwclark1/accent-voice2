# Copyright 2023 Accent Communications

from . import confd


def associate(user_id, funckey_template_id, check=True):
    response = confd.users(user_id).funckeys.templates(funckey_template_id).put()
    if check:
        response.assert_ok()


def dissociate(user_id, funckey_template_id, check=True):
    response = confd.users(user_id).funckeys.templates(funckey_template_id).delete()
    if check:
        response.assert_ok()
