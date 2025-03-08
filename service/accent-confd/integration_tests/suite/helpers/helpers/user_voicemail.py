# Copyright 2023 Accent Communications

from . import confd


def associate(user_id, voicemail_id, check=True):
    response = confd.users(user_id).voicemails(voicemail_id).put()
    if check:
        response.assert_ok()


def dissociate(user_id, voicemail_id, check=True):
    response = confd.users(user_id).voicemails.delete()
    if check:
        response.assert_ok()
