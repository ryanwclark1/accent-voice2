# Copyright 2023 Accent Communications

from . import confd


def associate(user_id, agent_id, check=True):
    response = confd.users(user_id).agents(agent_id).put()
    if check:
        response.assert_ok()


def dissociate(user_id, agent_id, check=True):
    response = confd.users(user_id).agents().delete()
    if check:
        response.assert_ok()
