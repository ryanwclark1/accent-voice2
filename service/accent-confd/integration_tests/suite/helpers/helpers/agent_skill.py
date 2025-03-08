# Copyright 2023 Accent Communications

from . import confd


def associate(agent_id, skill_id, **kwargs):
    check = kwargs.pop('check', True)
    response = confd.agents(agent_id).skills(skill_id).put(**kwargs)
    if check:
        response.assert_ok()


def dissociate(agent_id, skill_id, **kwargs):
    check = kwargs.get('check', True)
    response = confd.agents(agent_id).skills(skill_id).delete()
    if check:
        response.assert_ok()
